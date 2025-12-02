import wikipedia
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import sqlite3

# ----- Memory -----
memory_store = {}

def teach_brain(key, value):
    memory_store[key.lower()] = value
    return "Got it! I’ve learned that."

def search_memory(key):
    return memory_store.get(key.lower())

def delete_memory(key):
    return memory_store.pop(key.lower(), "Not found")

def load_memory():
    return memory_store


# ----- Main Answer Flow -----
def jarvis_answer(query):
    # 1. Check local memory
    memory = search_memory(query)
    if memory:
        return memory

    # 2. Try Wikipedia
    try:
        return wikipedia.summary(query, sentences=2)
    except Exception:
        pass

    # 3. Try Google
    try:
        for url in search(query, num=3, stop=3, pause=2):
            page = requests.get(url, timeout=5)
            soup = BeautifulSoup(page.text, 'html.parser')
            text = " ".join([p.get_text() for p in soup.find_all("p")][:3])
            if text.strip():
                return text[:400]  # limit long answers
    except Exception:
        pass

    # 4. Fallback
    return "Sorry, I couldn’t find that."


# ----- SQLite Memory DB -----
def init_brain():
    """Initialize the SQLite database for Jarvis brain."""
    conn = sqlite3.connect("jarvis_brain.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT
    )
    """)

    conn.commit()
    conn.close()
