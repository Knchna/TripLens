import os
import sqlite3
import pandas as pd
from scripts.chroma_sync import sync_package_to_chroma

DB_PATH = os.path.join("database", "triplens.db")

def insert_new_package(payload, sync_vector_db=True):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    pkg = payload["package"]
    p_id = pkg["package_id"]

    try:
        cursor.execute("""
            INSERT OR REPLACE INTO packages (
                package_id, agency_name, package_name, source_url_or_doc, data_source,
                destinations, start_location, duration_days, duration_nights, price,
                raw_price, list_price, tier_range_exists, transport_type, theme,
                suited_for, itinerary_pace, customizable, agency_contact
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p_id, pkg.get("agency_name"), pkg.get("package_name"),
            pkg.get("source_url_or_doc", "portal"), pkg.get("data_source", "packager_submission"),
            pkg.get("destinations"), pkg.get("start_location"), pkg.get("duration_days"),
            pkg.get("duration_nights"), pkg.get("price"), str(pkg.get("price")),
            pkg.get("list_price"), pkg.get("tier_range_exists", "FALSE"),
            pkg.get("transport_type"), pkg.get("theme"), pkg.get("suited_for"),
            pkg.get("itinerary_pace"), pkg.get("customizable", "TRUE"), pkg.get("agency_contact")
        ))

        cursor.execute("DELETE FROM itinerary_days WHERE package_id = ?", (p_id,))
        cursor.execute("DELETE FROM accommodation WHERE package_id = ?", (p_id,))
        cursor.execute("DELETE FROM inclusions WHERE package_id = ?", (p_id,))
        cursor.execute("DELETE FROM exclusions WHERE package_id = ?", (p_id,))

        for d in payload.get("itinerary_days", []):
            cursor.execute("""
                INSERT INTO itinerary_days (
                    package_id, day_number, stops, activities, activity_type,
                    distance_km, transit_hours, stops_requiring_separate_drives, meals_included_today
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p_id, d.get("day_number"), d.get("stops"), d.get("activities"),
                d.get("activity_type", "sightseeing"), d.get("distance_km", 0.0),
                d.get("transit_hours", 0.0), d.get("stops_requiring_separate_drives", 0),
                d.get("meals_included_today")
            ))

        for a in payload.get("accommodation", []):
            cursor.execute("""
                INSERT INTO accommodation (package_id, destination, accommodation_category, hotel_name, hotel_guaranteed)
                VALUES (?, ?, ?, ?, ?)
            """, (p_id, a.get("destination"), a.get("accommodation_category"), a.get("hotel_name", "unspecified"), a.get("hotel_guaranteed", "FALSE")))

        for inc in payload.get("inclusions", []):
            cursor.execute("INSERT INTO inclusions (package_id, inclusion_item) VALUES (?, ?)", (p_id, inc))

        for exc in payload.get("exclusions", []):
            cursor.execute("INSERT INTO exclusions (package_id, exclusion_item) VALUES (?, ?)", (p_id, exc))

        conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        raise RuntimeError(f"Package insertion failed: {e}")

    days_summary = "; ".join([f"Day {d.get('day_number')} ({d.get('stops')}): {d.get('activities')}" for d in payload.get("itinerary_days", [])])
    hotels_summary = ", ".join([f"{a.get('destination')} ({a.get('accommodation_category')})" for a in payload.get("accommodation", [])])
    
    canonical_doc = {
        "package_id": p_id,
        "package_name": pkg.get("package_name"),
        "start_location": pkg.get("start_location"),
        "duration_days": pkg.get("duration_days"),
        "price": pkg.get("price"),
        "total_transit_hours": sum([float(d.get("transit_hours", 0.0)) for d in payload.get("itinerary_days", [])]),
        "canonical_text": (
            f"Package: {pkg.get('package_name')} by {pkg.get('agency_name')}. "
            f"Start Location: {pkg.get('start_location')}. Destinations: {pkg.get('destinations')}. "
            f"Duration: {pkg.get('duration_days')} Days. Pace: {pkg.get('itinerary_pace')}. "
            f"Price: Rs {pkg.get('price')}. Daily Itinerary: {days_summary}. "
            f"Accommodations: {hotels_summary}."
        )
    }

    conn.close()

    if sync_vector_db:
        sync_package_to_chroma(canonical_doc)

    return canonical_doc
