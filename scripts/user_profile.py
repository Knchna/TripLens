import os
import sqlite3
import json

DB_PATH = os.path.join("database", "triplens.db")

def init_user_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id TEXT PRIMARY KEY,
            home_location TEXT DEFAULT 'Bangalore',
            personalization_enabled INTEGER DEFAULT 1,
            preferred_destinations_json TEXT DEFAULT '[]',
            visited_destinations_json TEXT DEFAULT '[]',
            preferred_themes_json TEXT DEFAULT '[]',
            preferred_pace_json TEXT DEFAULT '[]',
            preferred_transport_json TEXT DEFAULT '[]',
            preferred_budget_min REAL,
            preferred_budget_max REAL,
            preferred_duration_min INTEGER,
            preferred_duration_max INTEGER,
            travel_party_patterns_json TEXT DEFAULT '[]',
            avoided_preferences_json TEXT DEFAULT '[]',
            confidence_json TEXT DEFAULT '{}',
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS trip_history (
            trip_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            package_id TEXT,
            destinations_json TEXT NOT NULL,
            start_location TEXT,
            travel_date TEXT,
            duration_days INTEGER,
            budget_spent_inr REAL,
            travelers INTEGER,
            themes_json TEXT DEFAULT '[]',
            pace TEXT,
            transport TEXT,
            source TEXT DEFAULT 'triplens_package',
            user_rating REAL,
            user_feedback TEXT,
            liked_json TEXT DEFAULT '[]',
            disliked_json TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES user_profiles(user_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS recommendation_history (
            recommendation_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            package_id TEXT NOT NULL,
            recommendation_type TEXT DEFAULT 'next_trip',
            reason_codes_json TEXT DEFAULT '[]',
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_action TEXT DEFAULT 'viewed',
            FOREIGN KEY(user_id) REFERENCES user_profiles(user_id) ON DELETE CASCADE
        );
    """)

    # Ensure default user profile U001 exists
    cursor.execute("SELECT user_id FROM user_profiles WHERE user_id = 'U001'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO user_profiles (user_id, home_location) VALUES ('U001', 'Bangalore')")
    
    conn.commit()
    conn.close()

def get_user_profile(user_id="U001"):
    init_user_tables()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    return {
        "user_id": d["user_id"],
        "home_location": d["home_location"],
        "personalization_enabled": bool(d["personalization_enabled"]),
        "preferred_destinations": json.loads(d["preferred_destinations_json"] or "[]"),
        "visited_destinations": json.loads(d["visited_destinations_json"] or "[]"),
        "preferred_themes": json.loads(d["preferred_themes_json"] or "[]"),
        "preferred_pace": json.loads(d["preferred_pace_json"] or "[]"),
        "preferred_transport": json.loads(d["preferred_transport_json"] or "[]"),
        "preferred_budget_range": {
            "min": d["preferred_budget_min"],
            "max": d["preferred_budget_max"]
        },
        "preferred_duration_range": {
            "min_days": d["preferred_duration_min"],
            "max_days": d["preferred_duration_max"]
        },
        "travel_party_patterns": json.loads(d["travel_party_patterns_json"] or "[]"),
        "avoided_preferences": json.loads(d["avoided_preferences_json"] or "[]"),
        "confidence": json.loads(d["confidence_json"] or "{}"),
        "last_updated": d["last_updated"]
    }

def update_user_profile_settings(user_id="U001", settings: dict = None):
    init_user_tables()
    if not settings:
        return get_user_profile(user_id)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    fields = []
    params = []
    if "home_location" in settings:
        fields.append("home_location = ?")
        params.append(settings["home_location"])
    if "personalization_enabled" in settings:
        fields.append("personalization_enabled = ?")
        params.append(1 if settings["personalization_enabled"] else 0)
    if "avoided_preferences" in settings:
        fields.append("avoided_preferences_json = ?")
        params.append(json.dumps(settings["avoided_preferences"]))

    if fields:
        fields.append("last_updated = CURRENT_TIMESTAMP")
        query = f"UPDATE user_profiles SET {', '.join(fields)} WHERE user_id = ?"
        params.append(user_id)
        cursor.execute(query, params)
        conn.commit()
    conn.close()
    return get_user_profile(user_id)

def reset_user_history(user_id="U001"):
    init_user_tables()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trip_history WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM recommendation_history WHERE user_id = ?", (user_id,))
    cursor.execute("""
        UPDATE user_profiles SET
            preferred_destinations_json = '[]',
            visited_destinations_json = '[]',
            preferred_themes_json = '[]',
            preferred_pace_json = '[]',
            preferred_transport_json = '[]',
            preferred_budget_min = NULL,
            preferred_budget_max = NULL,
            preferred_duration_min = NULL,
            preferred_duration_max = NULL,
            travel_party_patterns_json = '[]',
            avoided_preferences_json = '[]',
            confidence_json = '{}',
            last_updated = CURRENT_TIMESTAMP
        WHERE user_id = ?
    """, (user_id,))
    conn.commit()
    conn.close()
    return get_user_profile(user_id)
