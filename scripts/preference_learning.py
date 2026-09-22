import os
import sqlite3
import json
from collections import Counter
from scripts.trip_history import get_trip_history
from scripts.user_profile import init_user_tables

DB_PATH = os.path.join("database", "triplens.db")

def refresh_user_preferences(user_id: str = "U001"):
    init_user_tables()
    history = get_trip_history(user_id)
    if not history:
        return

    visited_dests = []
    themes = []
    paces = []
    transports = []
    durations = []
    budgets = []
    disliked_items = []
    liked_items = []

    for trip in history:
        for d in trip["destinations"]:
            if d and d not in visited_dests:
                visited_dests.append(d)
        for t in trip["themes"]:
            if t:
                themes.append(t.lower())
        if trip["pace"]:
            paces.append(trip["pace"])
        if trip["transport"]:
            transports.append(trip["transport"])
        if trip["duration_days"]:
            durations.append(trip["duration_days"])
        if trip["budget_spent_inr"]:
            budgets.append(trip["budget_spent_inr"])
        for item in trip.get("liked", []):
            if item:
                liked_items.append(item.lower())
        for item in trip.get("disliked", []):
            if item:
                disliked_items.append(item.lower())

    theme_counts = Counter(themes + liked_items)
    top_themes = [item for item, _ in theme_counts.most_common(5)]

    pace_counts = Counter(paces)
    top_paces = [item for item, _ in pace_counts.most_common(3)]

    transport_counts = Counter(transports)
    top_transports = [item for item, _ in transport_counts.most_common(3)]

    min_budget = min(budgets) if budgets else None
    max_budget = max(budgets) if budgets else None

    min_duration = min(durations) if durations else None
    max_duration = max(durations) if durations else None

    disliked_counts = Counter(disliked_items)
    avoided = [item for item, count in disliked_counts.items() if count >= 1]

    total_trips = len(history)
    confidence = {}
    for t in top_themes:
        count = theme_counts[t]
        confidence[t] = round(min(0.95, 0.3 + (count / max(total_trips, 1)) * 0.6), 2)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE user_profiles SET
            visited_destinations_json = ?,
            preferred_themes_json = ?,
            preferred_pace_json = ?,
            preferred_transport_json = ?,
            preferred_budget_min = ?,
            preferred_budget_max = ?,
            preferred_duration_min = ?,
            preferred_duration_max = ?,
            avoided_preferences_json = ?,
            confidence_json = ?,
            last_updated = CURRENT_TIMESTAMP
        WHERE user_id = ?
    """, (
        json.dumps(visited_dests),
        json.dumps(top_themes),
        json.dumps(top_paces),
        json.dumps(top_transports),
        min_budget,
        max_budget,
        min_duration,
        max_duration,
        json.dumps(avoided),
        json.dumps(confidence),
        user_id
    ))
    conn.commit()
    conn.close()
