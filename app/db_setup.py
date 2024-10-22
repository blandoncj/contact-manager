from db.db_connection import DatabaseConnection

USERS_TABLE = """ 
    
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        nickname TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    ); 
"""

CONTACTS_TABLE = """

    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        lastname TEXT,
        email TEXT,
        address TEXT,
        type TEXT NOT NULL,
        is_favorite BOOLEAN NOT NULL DEFAULT 0,
        user_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );

"""

PHONES_TABLE = """
    
    CREATE TABLE IF NOT EXISTS phones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT NOT NULL,
        contact_id INTEGER NOT NULL,
        FOREIGN KEY(contact_id) REFERENCES contacts(id)
    
    );

"""

with DatabaseConnection() as conn:
    cursor = conn.cursor()
    cursor.execute(USERS_TABLE)
    cursor.execute(CONTACTS_TABLE)
    cursor.execute(PHONES_TABLE)
