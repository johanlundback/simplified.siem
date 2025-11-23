import sqlite3

DB_PATH = "database/siem.db"

def saveEvent(timestamp, message, riskLvl):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events (timestamp, message, riskLvL)
        VALUES (?, ?, ?)
    """, (timestamp, message, riskLvl))
    conn.commit()
    conn.close()

def latestEvents(limit=20):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, message, riskLvL
        FROM events
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows
