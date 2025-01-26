from sqlmodel import Session, select, SQLModel, Relationship
from Classes.icalendar import general
from database import engine
from datetime import datetime, date
from Classes.database import OperationDB

def generateLastDetectionIndex():
    return int(datetime.now().timestamp())

def main():
    lastDetectionIndex = generateLastDetectionIndex()
    general(engine, lastDetectionIndex)
    with Session(engine) as session:
        with OperationDB(session) as odb:
            odb.deleteObsoleteIndexes(lastDetectionIndex)

def tests():
    with Session(engine) as session:
        with OperationDB(session) as op:
            # op.changeLevel(["IE4-I41", "IE4-I42"], "IE4-I4")
            op.imageRec()

if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
    main()
