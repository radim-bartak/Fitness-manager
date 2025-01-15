import mysql.connector
from app.config import *

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def connect(self):
        if self._instance._connection is None:
            self._instance._connection = mysql.connector.connect(
                host = DB_HOST,
                user = DB_USER,
                password = DB_PASSWORD,
                database = DB_NAME
            )
        return self._instance._connection

    def close(self):
        if self._instance._connection is not None:
            self._instance._connection.close()
            self._instance._connection = None

db_connection = DatabaseConnection()
connection = db_connection.connect()

print(DATABASE_URI)
print("Pripojeno.")

connection.close()