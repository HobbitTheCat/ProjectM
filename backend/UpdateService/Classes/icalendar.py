from ics import Calendar
from sqlmodel import Session
from Models.model import Event, Location, Subgroup, Direction, Teacher, Year
from Classes.database import OperationDB
from datetime import datetime
from dotenv import load_dotenv, dotenv_values
import httpx, os, pytz, hashlib

def getYearFromDirection(directionName: str, odb, year = None):
    if year is None:
        semester = int(directionName[-1])
        if semester <= 2:
            year = odb.create_year(Year(name="L1"))
        elif semester <= 4:
            year = odb.create_year(Year(name="L2"))
        else:
            year = odb.create_year(Year(name="L3"))
        return year
    return year

def getDirectionFromSubgroup(subgroupName: str, odb):
    subgroup = subgroupName.split("-")[0]


"""
    Выполняет http запрос на сервер с расписанием
"""
def getEventsList(path):
    with httpx.Client() as client:
        response = client.get(path)
        calendar = Calendar(response.text)
    return calendar

"""
    Создание хэша из 
    Названия + Дня + Времени начала + Времени конца + локации + профессора + года + направления + подгруппы
"""
def createHash(event_icl):
    string = event_icl.name + str(event_icl.day) + str(event_icl.time_start) + str(event_icl.time_end)
    string += ''.join(map(str, event_icl.location))
    string += ''.join(map(str, event_icl.teacher))
    string += ''.join(map(str, event_icl.year))
    string += ''.join(map(str, event_icl.direction))
    string += ''.join(map(str, event_icl.subgroup))
    string.replace(' ', '')
    string = hashlib.sha256(string.encode()).hexdigest()
    return string

"""
    Создание объекта урока
    Добавить создание связей между группами
"""
def createObject(event_icl, odb, lastDetection, event_hash):

    locationList = []
    teacherList = []
    subgroupList =[]
    directionList = []
    yearList = []

    for location in event_icl.location:
        locObject = Location(name=location)
        status = odb.check_location_existence(locObject)
        locationList.append(status if status else locObject)

    for teacher in event_icl.teacher:
        teacherObject = Teacher(name=teacher)
        status = odb.check_teacher_existence(teacherObject)
        teacherList.append(status if status else teacherObject)

    for subgroup in event_icl.subgroup:
        subgroupObject = Subgroup(name=subgroup)                # добавить вычисление индекса направления
        status = odb.check_subgroup_existence(subgroupObject)
        subgroupList.append(status if status else subgroupObject)

    for direction in event_icl.direction:
        directionObject = Direction(name=direction, yearList=[getYearFromDirection(direction, odb)])             # добавить вычисление индекса года
        status = odb.check_direction_existence(directionObject)
        directionList.append(status if status else directionObject)

    for year in event_icl.year:
        yearObject = Year(name=year)
        status = odb.check_year_existence(yearObject)
        yearList.append(status if status else yearObject)

    return Event(
        day = event_icl.day,
        time_start = event_icl.time_start,
        time_end = event_icl.time_end,
        name = event_icl.name,

        last_detection = lastDetection,
        hash = event_hash,

        locations = locationList,
        teachers = teacherList,
        subgroups = subgroupList,
        directions = directionList,
        years = yearList,
    )
"""
    Эта функция создает хэш затем пытается найти событие по нему
    В случае успеха меняет индекс последнего обнаружения
    В случае неудачи передает поиск или создание объекта классу базы данных
"""
def searchEvent(event_icl, odb, lastDetection):
    event_hash = createHash(event_icl)
    eventObj = odb.check_event_existence_hash(event_hash)
    if eventObj:
        eventObj.last_detection = lastDetection
        return
    eventObj = createObject(event_icl, odb, lastDetection, event_hash)
    odb.create_event(eventObj) # тут происходит создание нового или дополнение старого объекта

"""
    Вносит новые поля в событие
    ДОПОЛНИТЬ ИСПРАВЛЕНЕИМ ПРЕДМЕТОВ И ЛОКАЦИЙ
"""
def eventModification(event_ics):
    begin = datetime.fromisoformat(str(event_ics.begin)).astimezone(pytz.timezone("Europe/Paris"))
    event_ics.time_end = datetime.fromisoformat(str(event_ics.end)).astimezone(pytz.timezone("Europe/Paris")).time()
    event_ics.day = begin.date()
    event_ics.time_start = begin.time()

    event_ics.description = event_ics.description.split("\n")[2:-2]
    event_ics.teacher = []
    event_ics.year = ''
    event_ics.direction = []
    event_ics.subgroup = []

    for ell in event_ics.description:
        if "Parcours" in ell:
            event_ics.direction.append(ell.replace("Parcours ", ""))
        elif not any(char.isdigit() for char in ell):
            event_ics.teacher.append(ell)
        elif " " not in ell:
            event_ics.subgroup.append(ell)
        else:
            event_ics.year = ell

def fullSearch(envName, lastDetection, engine):
    with Session(engine) as session:
        odb = OperationDB(session)
        c = getEventsList(os.getenv(envName))
        for event in c.events:
            eventModification(event)
            searchEvent(event, odb, lastDetection)

def general(engine):
    # load_dotenv() добавить эквивалентность некоторых названий
    config = dotenv_values()

    print(config.keys())
