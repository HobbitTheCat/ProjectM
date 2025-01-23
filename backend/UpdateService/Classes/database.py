from typing import Union

from sqlmodel import Session, select
from Models.model import *
from ics import Calendar
import datetime

class OperationDB:
    """
        Класс функций для работы с базой данных
    """

    def __init__(self, session: Session):
        self.session = session

    """
        Функции проверки существования (не предпринимают никах действий)
        В случае успеха возвращают первый из найденных объектов
        В случае неудачи None
    """

    def check_event_existence(self, event: Event):
        filters = {key: value for key, value in event.model_dump(exclude={"id", "location", "teacher", "year", "group", "subgroup"}).items() if value is not None}
        query = select(Event).filter_by(**filters)
        result = self.session.exec(query)
        return result.first()

    def check_event_existence_hash(self, event_hash:str):
        query = select(Event).where(Event.hash == event_hash)
        result = self.session.exec(query)
        return result

    def check_location_existence(self, location: Location):
        query = select(Location).filter_by(name=location.name)
        result = self.session.exec(query)
        return result.first()

    def check_teacher_existence(self, teacher: Teacher):
        query = select(Teacher).filter_by(name=teacher.name)
        result = self.session.exec(query)
        return result.first()

    def check_year_existence(self, year: Year):
        query = select(Year).filter_by(name=year.name)
        result = self.session.exec(query)
        return result.first()

    def check_direction_existence(self, direction: Direction):
        query = select(Direction).filter_by(name=direction.name)
        result = self.session.exec(query)
        return result.first()

    def check_subgroup_existence(self, subgroup: Subgroup):
        query = select(Subgroup).filter_by(name=subgroup.name)
        result = self.session.exec(query)
        return result.first()

    """
        Функции для создания новых объектов в базе данных
        В случае нахождения существующих объектов проверяют наличие всех атрибутов
    """

    def create_event(self, event: Event):
        dataBaseRec = self.check_event_existence(event)
        if  dataBaseRec is None:
            self.session.add(event)
        else:
            print("\nДобавление полей")
            dataBaseRec.add(event)

    def createYear(self, year: Year):
        dataBaseRec = self.check_year_existence(year)
        if dataBaseRec is None:
            self.session.add(year)
            return self.check_year_existence(year)
        return dataBaseRec

    def createSubgroup(self, subgroup: Subgroup):
        dataBaseRec = self.check_subgroup_existence(subgroup)
        if dataBaseRec is None:
            self.session.add(subgroup)
            return self.check_subgroup_existence(subgroup)
        return subgroup

    # добавить провреку на дубли