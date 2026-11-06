import sqlite3

DB_NAME = "students.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # lets us read columns by name
    return conn


def init_db():
    conn = get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                name    TEXT NOT NULL,
                email   TEXT NOT NULL UNIQUE,
                age     INTEGER NOT NULL,
                course  TEXT NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()