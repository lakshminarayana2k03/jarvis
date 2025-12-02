import sqlite3
import datetime

def init_db():
    conn = sqlite3.connect("jarvis.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS reminders (note TEXT, time TEXT)")
    conn.commit()
    conn.close()

def add_reminder(note):
    conn = sqlite3.connect("jarvis.db")
    c = conn.cursor()
    c.execute("INSERT INTO reminders VALUES (?, ?)", (note, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_reminders():
    conn = sqlite3.connect("jarvis.db")
    c = conn.cursor()
    c.execute("SELECT note, time FROM reminders")
    results = c.fetchall()
    conn.close()
    return results
