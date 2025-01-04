import sqlite3, os

DataBasePath = os.getenv('DATABASE_PATH')

class DataBase:

    def __init__(self):
        self.conn = sqlite3.connect(DataBasePath)
        self.cursor = self.conn.cursor()
        self.checkCreation()

    def checkCreation(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
            USER_NAME TEXT NOT NULL PRIMARY KEY,
            HASH TEXT NOT NULL,)
        ''')

    def existUser(self, USER_NAME):
        self.cursor.execute('SELECT * FROM Users WHERE USER_NAME = ?', (USER_NAME,))
        user = self.cursor.fetchone()
        if user:
            return True
        return False

    def insertUser(self, USER_NAME, HASH):
        if not self.existUser(USER_NAME):
            self.cursor.execute('INSERT INTO Users (USER_NAME, HASH) VALUES (?, ?)', (USER_NAME, HASH))
            return True
        return False

    def getHash(self, USER_NAME):
        if self.existUser(USER_NAME):
            self.cursor.execute('SELECT HASH FROM Users WHERE USER_NAME = ?', (USER_NAME,))
            return self.cursor.fetchone()[0]
        return None