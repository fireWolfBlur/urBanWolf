import sqlite3

def connector():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()  # Fixed typo here
    conn.execute("PRAGMA foreign_keys = ON")
    return conn, cursor

def users():
    conn, cursor = connector()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username TEXT,
            first_name TEXT,
            last_name TEXT
        )
    """)
    conn.commit()
    conn.close()

def conversations():
    conn, cursor = connector()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Conversations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            message_thread_id INTEGER,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES Users(user_id)
        )
    """)
    conn.commit()
    conn.close()

def events():
    conn, cursor = connector()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER UNIQUE,
            title TEXT,
            description TEXT,
            media TEXT,
            date_start TEXT,
            date_end TEXT,
            add_by INTEGER,
            keyboard JSON,
            FOREIGN KEY(add_by) REFERENCES Users(user_id)
        )
    """)
    conn.commit()
    conn.close()


users()
conversations()
events()

def alter():
    conn, cursor = connector()
    cursor.execute("ALTER TABLE Users ADD COLUMN in_proced TEXT DEFAULT 'None'")
    conn.commit()
    conn.close()