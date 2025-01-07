import sqlite3, os
from dotenv import load_dotenv

load_dotenv()
DataBasePath = os.getenv('DATABASE_PATH')


def checkCreation():
    conn = sqlite3.connect(DataBasePath)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        USER_NAME TEXT NOT NULL UNIQUE PRIMARY KEY,
        HASH TEXT NOT NULL)
    ''')
    conn.close()

class DataBase:

    def __init__(self):
        self.path = DataBasePath

    def __enter__(self):
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def existUser(self, USER_NAME):
        self.cursor.execute('SELECT * FROM Users WHERE USER_NAME = ?', (USER_NAME,))
        return self.cursor.fetchone() is not None

    def insertUser(self, USER_NAME, HASH):
        if not self.existUser(USER_NAME):
            self.cursor.execute('INSERT INTO Users (USER_NAME, HASH) VALUES (?, ?)', (USER_NAME, HASH,))
            self.conn.commit()
            return True
        return False

    def deleteUser(self, USER_NAME):
        if self.existUser(USER_NAME):
            self.cursor.execute('DELETE FROM Users WHERE USER_NAME = ?', (USER_NAME,))
            self.conn.commit()
            return True
        return False

    def getHash(self, USER_NAME):
        self.cursor.execute('SELECT HASH FROM Users WHERE USER_NAME = ?', (USER_NAME,))
        row = self.cursor.fetchone()
        return row[0] if row else None
