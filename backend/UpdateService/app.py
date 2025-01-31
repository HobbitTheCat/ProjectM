from sqlmodel import Session, SQLModel
from Classes.icalendar import general
from database import engine, engineA
from datetime import datetime
from Classes.database import OperationDB
from sqlalchemy import text

def generateLastDetectionIndex():
    return int(datetime.now().timestamp())

def main():
    lastDetectionIndex = generateLastDetectionIndex()
    general(engine, lastDetectionIndex)
    with Session(engine) as session:
        with OperationDB(session) as odb:
            odb.deleteObsoleteIndexes(lastDetectionIndex)

def grant_permission():
    with Session(engineA) as session:
        session.execute(text("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO update_service;"))
        session.execute(text("GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO update_service;"))

        session.execute(text("GRANT SELECT ON ALL TABLES IN SCHEMA public TO data_process;"))
        session.execute(text("GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO data_process;"))
        session.commit()

if __name__ == "__main__":
    SQLModel.metadata.create_all(engineA)
    grant_permission()
    main()
