import os
import re
import sqlite3
import pandas as pd

DB_PATH = os.path.join("database", "triplens.db")
candidates = [
    os.path.join("data", "Package_Details_India(final).xlsx"),
    os.path.join("data", "Package_Details_India.xlsx"),
    "Package_Details_India(final).xlsx",
    "Package_Details_India.xlsx"
]

EXCEL_PATH = None
for p in candidates:
    if os.path.exists(p):
        EXCEL_PATH = p
        break

if not EXCEL_PATH:
    raise FileNotFoundError("Could not find Package_Details_India(final).xlsx or Package_Details_India.xlsx in project or data/ folder.")

print(f"[INGESTION] Reading workbook from: {EXCEL_PATH}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

cursor.executescript("""
DROP TABLE IF EXISTS exclusions;
DROP TABLE IF EXISTS inclusions;
DROP TABLE IF EXISTS accommodation;
DROP TABLE IF EXISTS itinerary_days;
DROP TABLE IF EXISTS packages;

CREATE TABLE packages (
    package_id TEXT PRIMARY KEY,
    agency_name TEXT,
    package_name TEXT,
    source_url_or_doc TEXT,
    data_source TEXT,
    destinations TEXT,
    start_location TEXT,
    duration_days INTEGER,
    duration_nights INTEGER,
    price REAL,
    raw_price TEXT,
    list_price REAL,
    tier_range_exists TEXT,
    transport_type TEXT,
    theme TEXT,
    suited_for TEXT,
    itinerary_pace TEXT,
    customizable TEXT,
    agency_contact TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE itinerary_days (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id TEXT,
    day_number INTEGER,
    stops TEXT,
    activities TEXT,
    activity_type TEXT,
    distance_km REAL,
    transit_hours REAL,
    stops_requiring_separate_drives INTEGER,
    meals_included_today TEXT,
    flagged_for_verification TEXT,
    notes TEXT,
    FOREIGN KEY(package_id) REFERENCES packages(package_id) ON DELETE CASCADE
);

CREATE TABLE accommodation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id TEXT,
    destination TEXT,
    accommodation_category TEXT,
    hotel_name TEXT,
    hotel_guaranteed TEXT,
    FOREIGN KEY(package_id) REFERENCES packages(package_id) ON DELETE CASCADE
);

CREATE TABLE inclusions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id TEXT,
    inclusion_item TEXT,
    FOREIGN KEY(package_id) REFERENCES packages(package_id) ON DELETE CASCADE
);

CREATE TABLE exclusions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id TEXT,
    exclusion_item TEXT,
    source_url TEXT,
    FOREIGN KEY(package_id) REFERENCES packages(package_id) ON DELETE CASCADE
);
""")

xl = pd.ExcelFile(EXCEL_PATH)

def clean_num(val):
    if pd.isna(val): return None
    s = re.sub(r'[^\d.]', '', str(val).split('-')[0])
    try: return float(s)
    except: return None

df_pkg = pd.read_excel(xl, sheet_name='Packages').dropna(subset=['package_id'])
df_pkg = df_pkg[~df_pkg['package_id'].astype(str).str.contains(r'Unique|Links|example', case=False, na=False)]
df_pkg['package_id'] = df_pkg['package_id'].astype(str).str.strip()
df_pkg = df_pkg.drop_duplicates(subset=['package_id'])

df_pkg['raw_price'] = df_pkg['price'].astype(str)
df_pkg['price'] = df_pkg['price'].apply(clean_num)
df_pkg['duration_days'] = df_pkg['duration_days'].apply(clean_num)
df_pkg['duration_nights'] = df_pkg['duration_nights'].apply(clean_num)
df_pkg['list_price'] = df_pkg['list_price'].apply(clean_num)
if 'cutomizable' in df_pkg.columns:
    df_pkg = df_pkg.rename(columns={'cutomizable': 'customizable'})

pkg_cols = ['package_id', 'agency_name', 'package_name', 'source_url_or_doc', 'data_source', 
            'destinations', 'start_location', 'duration_days', 'duration_nights', 'price', 
            'raw_price', 'list_price', 'tier_range_exists', 'transport_type', 'theme', 
            'suited_for', 'itinerary_pace', 'customizable', 'agency_contact']
df_pkg[pkg_cols].to_sql('packages', conn, if_exists='append', index=False)
valid_ids = set(df_pkg['package_id'])

df_days = pd.read_excel(xl, sheet_name='Itinerary_Days').dropna(subset=['package_id'])
df_days['package_id'] = df_days['package_id'].astype(str).str.strip()
df_days = df_days[df_days['package_id'].isin(valid_ids)]
for col in ['day_number', 'distance_km', 'transit_hours', 'stops_requiring_separate_drives']:
    if col in df_days.columns:
        df_days[col] = df_days[col].apply(clean_num)
days_cols = ['package_id', 'day_number', 'stops', 'activities', 'activity_type', 'distance_km', 
             'transit_hours', 'stops_requiring_separate_drives', 'meals_included_today', 
             'flagged_for_verification', 'notes']
df_days[[c for c in days_cols if c in df_days.columns]].to_sql('itinerary_days', conn, if_exists='append', index=False)

df_acc = pd.read_excel(xl, sheet_name='Accommodation').dropna(subset=['package_id'])
df_acc['package_id'] = df_acc['package_id'].astype(str).str.strip()
df_acc = df_acc[df_acc['package_id'].isin(valid_ids)]
acc_cols = ['package_id', 'destination', 'accommodation_category', 'hotel_name', 'hotel_guaranteed']
df_acc[[c for c in acc_cols if c in df_acc.columns]].to_sql('accommodation', conn, if_exists='append', index=False)

df_inc = pd.read_excel(xl, sheet_name='Inclusions').dropna(subset=['package_id'])
df_inc['package_id'] = df_inc['package_id'].astype(str).str.strip()
df_inc = df_inc[df_inc['package_id'].isin(valid_ids)]
df_inc[['package_id', 'inclusion_item']].to_sql('inclusions', conn, if_exists='append', index=False)

df_exc = pd.read_excel(xl, sheet_name='Exclusions').dropna(subset=['package_id'])
df_exc['package_id'] = df_exc['package_id'].astype(str).str.strip()
df_exc = df_exc[df_exc['package_id'].isin(valid_ids)]
if 'Unnamed: 2' in df_exc.columns:
    df_exc = df_exc.rename(columns={'Unnamed: 2': 'source_url'})
exc_cols = ['package_id', 'exclusion_item'] + (['source_url'] if 'source_url' in df_exc.columns else [])
df_exc[exc_cols].to_sql('exclusions', conn, if_exists='append', index=False)

conn.commit()
print("[SETUP COMPLETED] 5 relational tables initialized successfully.")
conn.close()
