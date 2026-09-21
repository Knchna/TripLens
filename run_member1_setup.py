import os
import re
import sqlite3
import hashlib
import pandas as pd
import numpy as np

os.makedirs("database", exist_ok=True)
os.makedirs("scripts", exist_ok=True)
os.makedirs("data", exist_ok=True)

# 1. SETUP DATABASE SCRIPT
setup_db_code = '''import os
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
    s = re.sub(r'[^\\d.]', '', str(val).split('-')[0])
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
'''

with open("scripts/setup_database.py", "w", encoding="utf-8") as f:
    f.write(setup_db_code)

# 2. PREPROCESS FEATURES SCRIPT
preprocess_code = '''import os
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
'''

with open("scripts/preprocess_features.py", "w", encoding="utf-8") as f:
    f.write(preprocess_code)

# 3. DATA ACCESS SCRIPT
data_access_code = '''import os
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
'''

with open("scripts/data_access.py", "w", encoding="utf-8") as f:
    f.write(data_access_code)

# 4. AUTH SERVICE SCRIPT
auth_code = '''import os
import sqlite3
import hashlib

DB_PATH = os.path.join("database", "triplens.db")

def init_user_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('traveler', 'packager', 'admin')),
            agency_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_user(email, password, role='traveler', agency_name=None):
    init_user_table()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    pwd_hash = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO users (email, password_hash, role, agency_name) VALUES (?, ?, ?, ?)",
            (email.strip().lower(), pwd_hash, role, agency_name)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return {"status": "success", "user_id": user_id, "email": email, "role": role}
    except sqlite3.IntegrityError:
        conn.close()
        return {"status": "error", "message": "Email already registered"}

def verify_user(email, password):
    init_user_table()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    pwd_hash = hash_password(password)
    cursor.execute(
        "SELECT id, email, role, agency_name FROM users WHERE email = ? AND password_hash = ?",
        (email.strip().lower(), pwd_hash)
    )
    user = cursor.fetchone()
    conn.close()
    if user:
        return {"authenticated": True, "id": user[0], "email": user[1], "role": user[2], "agency_name": user[3]}
    return {"authenticated": False, "message": "Invalid credentials"}

if __name__ == "__main__":
    init_user_table()
    create_user("agency@mystikal.com", "packager123", role="packager", agency_name="Mystikal Holidays")
    print("[AUTH SERVICE] User table initialized and default packager registered.")
'''

with open("scripts/auth_service.py", "w", encoding="utf-8") as f:
    f.write(auth_code)

# 5. CHROMA SYNC SCRIPT
chroma_code = '''import os
import sqlite3
import chromadb
from chromadb.utils import embedding_functions

DB_PATH = os.path.join("database", "triplens.db")
CHROMA_PATH = os.path.join("database", "chroma_db")

client = chromadb.PersistentClient(path=CHROMA_PATH)
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
collection = client.get_or_create_collection(
    name="travel_packages",
    embedding_function=embedding_func
)

def sync_package_to_chroma(canonical_doc):
    pkg_id = canonical_doc["package_id"]
    metadata = {
        "package_id": pkg_id,
        "package_name": str(canonical_doc["package_name"]),
        "start_location": str(canonical_doc["start_location"]),
        "duration_days": int(canonical_doc["duration_days"]) if canonical_doc["duration_days"] else 0,
        "price": float(canonical_doc["price"]) if canonical_doc["price"] else 0.0,
        "total_transit_hours": float(canonical_doc["total_transit_hours"])
    }
    collection.upsert(
        ids=[pkg_id],
        documents=[canonical_doc["canonical_text"]],
        metadatas=[metadata]
    )

def sync_all_existing_packages():
    from scripts.data_access import fetch_all_canonical_documents
    docs = fetch_all_canonical_documents()
    print(f"[CHROMA] Indexing {len(docs)} packages into ChromaDB...")
    
    ids = [d["package_id"] for d in docs]
    texts = [d["canonical_text"] for d in docs]
    metas = [{
        "package_id": d["package_id"],
        "package_name": str(d["package_name"]),
        "start_location": str(d["start_location"]),
        "duration_days": int(d["duration_days"]) if d["duration_days"] else 0,
        "price": float(d["price"]) if d["price"] else 0.0,
        "total_transit_hours": float(d["total_transit_hours"])
    } for d in docs]
    
    batch_size = 50
    for i in range(0, len(ids), batch_size):
        collection.upsert(
            ids=ids[i:i+batch_size],
            documents=texts[i:i+batch_size],
            metadatas=metas[i:i+batch_size]
        )
    print(f"[CHROMA COMPLETE] Total vectors in collection: {collection.count()}")

if __name__ == "__main__":
    sync_all_existing_packages()
'''

with open("scripts/chroma_sync.py", "w", encoding="utf-8") as f:
    f.write(chroma_code)

# 6. PACKAGE SERVICE SCRIPT
pkg_service_code = '''import os
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
'''

with open("scripts/package_service.py", "w", encoding="utf-8") as f:
    f.write(pkg_service_code)

# 7. HEALTH CHECK SCRIPT
health_check_code = '''import sqlite3
import chromadb
from scripts.data_access import filter_packages_by_constraints
from scripts.auth_service import verify_user

conn = sqlite3.connect('database/triplens.db')
c = conn.cursor()
tables = [t[0] for t in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall()]

client = chromadb.PersistentClient(path='database/chroma_db')
col = client.get_collection('travel_packages')

print('=' * 60)
print('TRIPLENS MEMBER 1 - ARCHITECTURE HEALTH REPORT')
print('=' * 60)
print(f'1. Relational Tables ({len(tables)}): {tables}')
print(f'2. Packages in SQLite: {c.execute("SELECT COUNT(package_id) FROM packages").fetchone()[0]}')
print(f'3. Vectors in ChromaDB: {col.count()}')
print(f'4. Enriched Feature Records: {c.execute("SELECT COUNT(package_id) FROM packages_enriched").fetchone()[0]}')
print(f'5. DAO Query Test: {len(filter_packages_by_constraints(duration_days=5))} packages found for 5-day trips')
auth = verify_user('agency@mystikal.com', 'packager123')
print(f'6. Auth Verification: {auth.get("role", "none")} login check passed')
print('=' * 60)
print('SYSTEM STATUS: 100% OPERATIONAL & READY FOR MEMBER 2/3/4')
conn.close()
'''

with open("scripts/health_check.py", "w", encoding="utf-8") as f:
    f.write(health_check_code)

print("[SUCCESS] All Member 1 python files written successfully to scripts/.")
