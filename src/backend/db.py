import sqlite3
import datetime

class DatabaseManager:
    def __init__(self, db_path='monitoring_service.db'):
        self.db_path = db_path
        self.setup_database()

    def get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def setup_database(self):
        conn = self.get_db_connection()
        conn.execute('PRAGMA journal_mode=WAL;')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS monitored_pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_name TEXT NOT NULL,
                page_url TEXT NOT NULL UNIQUE,
                start_monitoring TIMESTAMP NOT NULL,
                element_to_monitor TEXT,
                last_update TIMESTAMP,
                last_check TIMESTAMP,
                page_state TEXT,
                last_content TEXT,
                check_interval INTEGER NOT NULL
            );
        ''')
        conn.commit()
        conn.close()

    def add_page_to_monitor(self, name, url, element, interval, hashed_content):
        conn = self.get_db_connection()
        now = datetime.datetime.now()
        try:
            cursor = conn.execute(
                'INSERT INTO monitored_pages (page_name, page_url, start_monitoring, element_to_monitor, last_update, last_check, page_state, check_interval, last_content) VALUES (?,?,?,?,?,?,?,?,?)',
                (name, url, now, element, now, now, "ok", interval, hashed_content)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Errore: " + str(e))
            return None
        finally:
            conn.close()

    def update_page_status(self, id, new_state):
        conn = self.get_db_connection()
        conn.execute(
            'UPDATE monitored_pages SET last_check =?, page_state =? WHERE id =?',
            (datetime.datetime.now(), new_state, id)
        )
        conn.commit()
        conn.close()

    def update_page_content(self, id, hashed_content):
        conn = self.get_db_connection()
        conn.execute(
            'UPDATE monitored_pages SET last_content =?, last_update=? WHERE id =?',
            (hashed_content, datetime.datetime.now(), id)
        )
        conn.commit()
        conn.close()

    def get_all_pages_to_monitor(self):
        conn = self.get_db_connection()
        pages = conn.execute('SELECT * FROM monitored_pages').fetchall()
        conn.close()
        return pages

    def get_hashed_content(self, id):
        conn = self.get_db_connection()
        page = conn.execute('SELECT last_content FROM monitored_pages WHERE id = ?', (id,)).fetchone()
        conn.close()
        return page['last_content'] if page else None
    
    def get_page_by_id(self, id):
        conn = self.get_db_connection()
        page = conn.execute('SELECT * FROM monitored_pages WHERE id = ?', (id,)).fetchone()
        conn.close()
        return page if page else None
    
    def delete_page(self, id):
        conn = self.get_db_connection()
        conn.execute('DELETE FROM monitored_pages WHERE id = ?', (id,))
        conn.commit()
        conn.close()

    def update_page(self, id, name, url, interval):
        conn = self.get_db_connection()
        conn.execute(
            'UPDATE monitored_pages SET page_name=?, page_url=?, check_interval=? WHERE id=?',
            (name, url, interval, id)
        )
        conn.commit()
        conn.close()