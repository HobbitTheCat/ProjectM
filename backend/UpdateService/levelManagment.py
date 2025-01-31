from sqlmodel import Session
from Classes.database import OperationDB
from database import engine

def main():
    with Session(engine) as session:
        with OperationDB(session) as op:
            op.imageRec()
            op.createLevelStructure()
            op.imageRec()

if __name__ == "__main__":
    main()