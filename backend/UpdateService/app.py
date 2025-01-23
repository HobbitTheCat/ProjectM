from sqlmodel import Session, select
from Classes.icalendar import general
from database import engine
from Models.model import *
from Classes.database import OperationDB

def main():
    with Session(engine) as session:
        location = Location(name="A121")
        # event = Event(day=datetime.date(2025, 1, 20), time_start=datetime.time(10, 15),
        #               time_end=datetime.time(12, 15), name="Math4B",last_detection=0, location=[location])
        # event2 = Event(day=datetime.date(2025, 1, 21), time_start=datetime.time(10, 15),
        #                time_end=datetime.time(12, 15), name="Math4C",last_detection=0, location=[location])
        session.add(location)
        op = OperationDB(session)
        print("Проверка прошла результат: ", op.check_location_existence(location))

    #     op.create_event(event2)
    #
    #     # op.create_event(event2)
    #     # session.commit()
    #     # event2 = op.check_event_existence(event2)
    #
    #
    #     # event = op.check_event_existence(event)
    #     # print(event.location)
    #
    #     # session.delete(event)
    #     session.commit()


if __name__ == "__main__":
    # SQLModel.metadata.create_all(engine)
    main()
    # general(engine)