import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'smart_gate.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')

class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self._initialize_db()

    def _initialize_db(self):
        with open(SCHEMA_PATH, 'r') as f:
            self.cursor.executescript(f.read())
        self.conn.commit()

    def add_user(self, name):
        self.cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def log_access(self, user_id, status, confidence=None, image_path=None):
        self.cursor.execute(
            "INSERT INTO access_logs (user_id, status, confidence, image_path) VALUES (?, ?, ?, ?)",
            (user_id, status, confidence, image_path)
        )
        self.conn.commit()

    def get_last_access(self, user_id):
        self.cursor.execute(
            "SELECT timestamp FROM access_logs WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1",
            (user_id,)
        )
        return self.cursor.fetchone()

    def get_all_logs(self):
        self.cursor.execute("""
            SELECT l.id, u.name, l.timestamp, l.status, l.confidence 
            FROM access_logs l 
            LEFT JOIN users u ON l.user_id = u.id 
            ORDER BY l.timestamp DESC
        """)
        return self.cursor.fetchall()

    def update_user(self, user_id, new_name):
        self.cursor.execute("UPDATE users SET name = ? WHERE id = ?", (new_name, user_id))
        self.conn.commit()

    def delete_user(self, user_id):
        # Delete logs first due to foreign key (or rely on cascading if set)
        self.cursor.execute("DELETE FROM access_logs WHERE user_id = ?", (user_id,))
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = DBManager()
    print("Database initialized successfully.")
    users = db.get_users()
    print(f"Current users: {users}")
    db.close()
