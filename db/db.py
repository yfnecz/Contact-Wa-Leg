import sqlite3

class Database:
    def __init__(self):
        conn = sqlite3.connect("ai_cache.db")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ai_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                response TEXT
            )
        """)
        conn.close()

    def get_db(self):
        conn = sqlite3.connect("ai_cache.db")
        return conn

    def get_random_cached_response(self):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("SELECT response FROM ai_cache ORDER BY RANDOM() LIMIT 1")
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None

    def cache_response(self, response):
        conn = self.get_db()
        conn.execute("INSERT INTO ai_cache (response) VALUES (?)", (response,))
        conn.commit()
        conn.close()