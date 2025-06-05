import sqlite3

class Database:
    def __init__(self, db_path="ai_cache.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ai_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    response TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS usage_counter (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    count INTEGER
                )
            """)
            # Ensure a row exists
            conn.execute("INSERT OR IGNORE INTO usage_counter (id, count) VALUES (1, 0)")

    def cache_response(self, response, max_entries=100):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            # Count current entries
            cur.execute("SELECT COUNT(*) FROM ai_cache")
            count = cur.fetchone()[0]
            if count >= max_entries:
                # Delete the oldest entry
                cur.execute("DELETE FROM ai_cache WHERE id = (SELECT id FROM ai_cache ORDER BY timestamp ASC LIMIT 1)")
            # Insert the new response
            cur.execute("INSERT INTO ai_cache (response) VALUES (?)", (response,))
            conn.commit()

    def get_random_cached_response(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT response FROM ai_cache ORDER BY RANDOM() LIMIT 1")
            row = cur.fetchone()
            return row[0] if row else None

    def increment_usage(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE usage_counter SET count = count + 1 WHERE id = 1")
            conn.commit()

    def get_usage_count(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT count FROM usage_counter WHERE id = 1")
            row = cur.fetchone()
            return row[0] if row else 0