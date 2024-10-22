import sqlite3 as sql


class DatabaseConnection:
    def __init__(self) -> None:
        self.connection = self.connect()

    def __enter__(self) -> sql.Connection:
        self.connection = self.connect()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close_connection()

    def connect(self) -> sql.Connection:
        try:
            connection = sql.connect("database.db")
            return connection
        except sql.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def close_connection(self):
        if self.connection:
            self.connection.close()
