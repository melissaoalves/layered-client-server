import sqlite3
from datetime import datetime

DB_PATH = 'database/images.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            filter TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_image_metadata(filename, filter_type):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO images (filename, filter, timestamp) VALUES (?, ?, ?)",
        (filename, filter_type, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
