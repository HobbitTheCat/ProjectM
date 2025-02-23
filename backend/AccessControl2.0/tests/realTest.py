from database.postgres import engineA
from sqlmodel import Session
from sqlalchemy import text

def deleteAll():
    with Session(engineA) as session:
        session.execute(text("DELETE FROM session"))
        session.execute(text("DELETE FROM superman"))
        session.commit()

if __name__ == "__main__":
    deleteAll()