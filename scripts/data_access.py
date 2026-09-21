import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join("database", "triplens.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_canonical_documents():
    conn = get_db_connection()
    df_pkgs = pd.read_sql("SELECT * FROM packages", conn)
    df_days = pd.read_sql("SELECT * FROM itinerary_days ORDER BY package_id, day_number", conn)
    df_acc = pd.read_sql("SELECT * FROM accommodation", conn)
    df_inc = pd.read_sql("SELECT * FROM inclusions", conn)
    df_exc = pd.read_sql("SELECT * FROM exclusions", conn)
    conn.close()

    canonical_list = []
    for _, pkg in df_pkgs.iterrows():
        p_id = pkg["package_id"]
        days = df_days[df_days["package_id"] == p_id]
        accs = df_acc[df_acc["package_id"] == p_id]
        incs = df_inc[df_inc["package_id"] == p_id]
        excs = df_exc[df_exc["package_id"] == p_id]

        day_text = "; ".join([f"Day {r['day_number']} ({r['stops']}): {r['activities']}" for _, r in days.iterrows()]) or "Standard activities"
        acc_text = ", ".join([f"{r['destination']} ({r['accommodation_category'] or 'Standard'})" for _, r in accs.iterrows()]) or "Hotel details per booking"
        inc_text = ", ".join(incs["inclusion_item"].dropna().tolist()) or "Standard package inclusions"
        exc_text = ", ".join(excs["exclusion_item"].dropna().tolist()) or "Personal expenses excluded"

        canonical_text = (
            f"Package: {pkg['package_name']} by {pkg['agency_name']}. "
            f"Departs from: {pkg['start_location']}. Destinations: {pkg['destinations']}. "
            f"Duration: {pkg['duration_days']} Days / {pkg['duration_nights']} Nights. "
            f"Theme: {pkg['theme']}. Suited for: {pkg['suited_for']}. "
            f"Pace: {pkg['itinerary_pace']}. Transport: {pkg['transport_type']}. "
            f"Price: Rs {pkg['price']}. Daily Itinerary: {day_text}. "
            f"Hotels: {acc_text}. Inclusions: {inc_text}. Exclusions: {exc_text}."
        )

        canonical_list.append({
            "package_id": p_id,
            "package_name": pkg["package_name"],
            "start_location": pkg["start_location"],
            "duration_days": pkg["duration_days"],
            "price": pkg["price"],
            "canonical_text": canonical_text,
            "total_transit_hours": float(days["transit_hours"].fillna(0).sum())
        })
    return canonical_list

def filter_packages_by_constraints(start_location=None, max_price=None, duration_days=None, theme=None):
    conn = get_db_connection()
    query = "SELECT * FROM packages WHERE 1=1"
    params = []
    if start_location:
        query += " AND LOWER(start_location) LIKE ?"
        params.append(f"%{start_location.lower().strip()}%")
    if max_price:
        query += " AND price <= ?"
        params.append(float(max_price))
    if duration_days:
        query += " AND duration_days = ?"
        params.append(int(duration_days))
    if theme:
        query += " AND LOWER(theme) LIKE ?"
        params.append(f"%{theme.lower().strip()}%")
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df.to_dict(orient="records")

def get_itinerary_metrics(package_id):
    conn = get_db_connection()
    df = pd.read_sql(
        "SELECT day_number, transit_hours, distance_km, stops, stops_requiring_separate_drives "
        "FROM itinerary_days WHERE package_id = ? ORDER BY day_number",
        conn, params=[package_id]
    )
    conn.close()
    return df.to_dict(orient="records")
