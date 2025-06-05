import sqlite3, os

class Database:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.environ.get("AI_CACHE_DB_PATH", "/data/ai_cache.db")
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS usage_counter (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    count INTEGER
                )
            """)
            # Ensure a row exists
            conn.execute("INSERT OR IGNORE INTO usage_counter (id, count) VALUES (1, 0)")

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