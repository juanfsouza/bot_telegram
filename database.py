import sqlite3

class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_keys_table(self):
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS keys (
                    key TEXT PRIMARY KEY,
                    used BOOLEAN NOT NULL
                )
            ''')
            conn.commit()

    def add_key(self, key):
        with self._get_connection() as conn:
            c = conn.cursor()
            try:
                c.execute('INSERT INTO keys (key, used) VALUES (?, ?)', (key, False))
                conn.commit()
            except sqlite3.IntegrityError:
                print(f"A chave '{key}' já existe.")

    def validate_key(self, key):
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute('SELECT used FROM keys WHERE key = ?', (key,))
            row = c.fetchone()
            if row:
                return not row[0]
            return False

    def use_key(self, key):
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute('UPDATE keys SET used = ? WHERE key = ?', (True, key))
            conn.commit()
