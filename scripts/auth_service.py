import os
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
