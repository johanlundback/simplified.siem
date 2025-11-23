from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from database.models import latestEvents
import sqlite3
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return HTMLResponse("<h1>SIEM API is running</h1><p>Use /events/latest</p>")

@app.get("/events/latest")
def latest_events():
    return latestEvents()


# New endpoint for Attack Timeline
@app.get("/stats/timeline")
def attack_timeline():

    conn = sqlite3.connect("database/siem.db")
    cursor = conn.cursor()

    # get last 60 minutes of data
    one_hour_ago = (datetime.now() - timedelta(minutes=60)).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        SELECT timestamp FROM events
        WHERE timestamp >= ?
        ORDER BY timestamp ASC
    """, (one_hour_ago,))

    rows = cursor.fetchall()
    conn.close()

    timeline = {}

    for (timestamp,) in rows:
        t = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        key = t.strftime("%H:%M")  # minute resolution

        timeline[key] = timeline.get(key, 0) + 1

    #returnera sorterat
    sorted_timeline = [{"time": k, "count": timeline[k]} for k in sorted(timeline.keys())]

    return sorted_timeline
