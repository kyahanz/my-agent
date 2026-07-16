import sqlite3
import json
from datetime import datetime

DB_PATH = "memory/agent_memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            role TEXT,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_message(role: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversations (timestamp, role, content) VALUES (?, ?, ?)",
        (datetime.now().isoformat(), role, content)
    )
    conn.commit()
    conn.close()

def load_history(limit: int = 20) -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM conversations ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    # Balik urutannya biar dari yang lama ke baru
    rows.reverse()
    
    return [{"role": row[0], "content": row[1]} for row in rows]

def clear_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM conversations")
    conn.commit()
    conn.close()
    return "✅ Memory berhasil dihapus."