### Response (time: 20240204211613)

{
    "file_path": "/src/database.py",
    "code": "import sqlite3\n\nclass DatabaseManager:\n    def __init__(self, db_name):\n        self.conn = sqlite3.connect(db_name)\n        self.cur = self.conn.cursor()\n\n    def execute_query(self, query):\n        self.cur.execute(query)\n        self.conn.commit()\n\n    def fetch_data(self, query):\n        self.cur.execute(query)\n        return self.cur.fetchall()\n\n    def close_connection(self):\n        self.conn.close()",
    "file_instruction": "This file manages database connections and operations using SQLite. To use the file, create an instance of DatabaseManager with the database name, execute queries using execute_query method, fetch data using fetch_data method, and close the connection when done using close_connection method."
}