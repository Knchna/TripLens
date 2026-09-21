import os
import sqlite3
import pandas as pd
import numpy as np

DB_PATH = os.path.join("database", "triplens.db")
conn = sqlite3.connect(DB_PATH)

df_pkg = pd.read_sql("SELECT * FROM packages", conn)
df_days = pd.read_sql("SELECT * FROM itinerary_days", conn)
df_acc = pd.read_sql("SELECT * FROM accommodation", conn)
df_inc = pd.read_sql("SELECT * FROM inclusions", conn)
df_exc = pd.read_sql("SELECT * FROM exclusions", conn)

itinerary_agg = df_days.groupby("package_id").agg(
    total_transit_hours=("transit_hours", "sum"),
    total_distance_km=("distance_km", "sum"),
    total_stops=("stops", "count"),
    avg_transit_per_day=("transit_hours", "mean"),
    max_transit_day=("transit_hours", "max"),
    total_drives=("stops_requiring_separate_drives", "sum")
).reset_index()

acc_agg = df_acc.groupby("package_id").agg(hotel_count=("destination", "count")).reset_index()
inc_agg = df_inc.groupby("package_id").agg(inclusion_count=("inclusion_item", "count")).reset_index()
exc_agg = df_exc.groupby("package_id").agg(exclusion_count=("exclusion_item", "count")).reset_index()

df_feat = df_pkg.merge(itinerary_agg, on="package_id", how="left")
df_feat = df_feat.merge(acc_agg, on="package_id", how="left")
df_feat = df_feat.merge(inc_agg, on="package_id", how="left")
df_feat = df_feat.merge(exc_agg, on="package_id", how="left")

fill_zero_cols = [
    "total_transit_hours", "total_distance_km", "total_stops",
    "avg_transit_per_day", "max_transit_day", "total_drives",
    "hotel_count", "inclusion_count", "exclusion_count"
]
df_feat[fill_zero_cols] = df_feat[fill_zero_cols].fillna(0.0)

df_feat["price_per_day"] = np.where(
    (df_feat["price"].notna()) & (df_feat["duration_days"] > 0),
    (df_feat["price"] / df_feat["duration_days"]).round(2),
    np.nan
)
df_feat["destination_count"] = df_feat["destinations"].apply(
    lambda x: len(str(x).split(",")) if pd.notna(x) else 0
)
df_feat["theme_clean"] = df_feat["theme"].astype(str).str.lower().str.strip()
df_feat["transport_category"] = df_feat["transport_type"].apply(
    lambda x: "private" if "private" in str(x).lower()
    else ("shared" if any(w in str(x).lower() for w in ["shared", "bus", "volvo", "tempo"]) else "mixed_or_unspecified")
)

def assign_pace(row):
    pace = str(row["itinerary_pace"]).lower().strip()
    if "relaxed" in pace: return "Relaxed"
    if "moderate" in pace: return "Moderate"
    if "packed" in pace or "fast" in pace: return "Packed"
    if row["avg_transit_per_day"] >= 4.0 or row["total_stops"] > (row["duration_days"] * 2):
        return "Packed"
    elif row["avg_transit_per_day"] <= 2.0:
        return "Relaxed"
    return "Moderate"

df_feat["itinerary_pace_inferred"] = df_feat.apply(assign_pace, axis=1)

quality_fields = ["price", "duration_days", "start_location", "destinations", "transport_type", "theme"]
df_feat["data_completeness_score"] = (
    df_feat[quality_fields].notna().sum(axis=1) / len(quality_fields) * 100
).round(1)

df_feat.to_sql("packages_enriched", conn, if_exists="replace", index=False)
conn.commit()
conn.close()
print("[FEATURE ENGINEERING] Table 'packages_enriched' generated.")
