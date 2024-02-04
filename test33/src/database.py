import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def execute_query(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def fetch_data(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def close_connection(self):
        self.conn.close()