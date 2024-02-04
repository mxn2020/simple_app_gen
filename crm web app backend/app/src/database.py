import sqlite3

# Establish connection to SQLite database
def connect_to_database():
    conn = sqlite3.connect('crm_database.db')
    return conn

# Create user table in the database
def create_user_table():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()