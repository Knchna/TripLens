import os
import sqlite3
import json
import uuid
from scripts.user_profile import init_user_tables, get_user_profile

DB_PATH = os.path.join("database", "triplens.db")

def add_completed_trip(trip_data: dict, user_id: str = "U001"):
    init_user_tables()
    trip_id = trip_data.get("trip_id") or f"TRIP_{uuid.uuid4().hex[:8].upper()}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    destinations = trip_data.get("destination") or trip_data.get("destinations") or []
    if isinstance(destinations, str):
        destinations = [d.strip() for d in destinations.split(",") if d.strip()]

    themes = trip_data.get("themes") or []
    if isinstance(themes, str):
        themes = [t.strip() for t in themes.split(",") if t.strip()]

    liked = trip_data.get("liked") or []
    disliked = trip_data.get("disliked") or []

    cursor.execute("""
        INSERT OR REPLACE INTO trip_history (
            trip_id, user_id, package_id, destinations_json, start_location, travel_date,
            duration_days, budget_spent_inr, travelers, themes_json, pace, transport,
            source, user_rating, user_feedback, liked_json, disliked_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        trip_id,
        user_id,
        trip_data.get("package_id"),
        json.dumps(destinations),
        trip_data.get("start_location"),
        trip_data.get("travel_date"),
        trip_data.get("duration_days"),
        trip_data.get("budget_spent_inr") or trip_data.get("price"),
        trip_data.get("travelers"),
        json.dumps(themes),
        trip_data.get("pace"),
        trip_data.get("transport"),
        trip_data.get("source", "triplens_package"),
        trip_data.get("user_rating"),
        trip_data.get("user_feedback", ""),
        json.dumps(liked),
        json.dumps(disliked)
    ))

    conn.commit()
    conn.close()

    # Automatically trigger preference learning refresh
    from scripts.preference_learning import refresh_user_preferences
    refresh_user_preferences(user_id)

    return get_trip_history(user_id, trip_id=trip_id)[0]

def get_trip_history(user_id: str = "U001", trip_id: str = None):
    init_user_tables()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    if trip_id:
        rows = conn.execute("SELECT * FROM trip_history WHERE user_id = ? AND trip_id = ? ORDER BY created_at DESC", (user_id, trip_id)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM trip_history WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
    conn.close()

    result = []
    for r in rows:
        d = dict(r)
        result.append({
            "trip_id": d["trip_id"],
            "user_id": d["user_id"],
            "package_id": d["package_id"],
            "destinations": json.loads(d["destinations_json"] or "[]"),
            "start_location": d["start_location"],
            "travel_date": d["travel_date"],
            "duration_days": d["duration_days"],
            "budget_spent_inr": d["budget_spent_inr"],
            "travelers": d["travelers"],
            "themes": json.loads(d["themes_json"] or "[]"),
            "pace": d["pace"],
            "transport": d["transport"],
            "source": d["source"],
            "user_rating": d["user_rating"],
            "user_feedback": d["user_feedback"],
            "liked": json.loads(d["liked_json"] or "[]"),
            "disliked": json.loads(d["disliked_json"] or "[]"),
            "created_at": d["created_at"]
        })
    return result

def delete_trip_entry(trip_id: str, user_id: str = "U001"):
    init_user_tables()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trip_history WHERE trip_id = ? AND user_id = ?", (trip_id, user_id))
    conn.commit()
    conn.close()

    from scripts.preference_learning import refresh_user_preferences
    refresh_user_preferences(user_id)
    return {"status": "deleted", "trip_id": trip_id}
