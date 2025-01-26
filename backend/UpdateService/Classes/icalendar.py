from ics import Calendar
from sqlmodel import Session
from Models.model import Event, Location, Teacher, GroupTree
from Classes.database import OperationDB
from datetime import datetime
from dotenv import dotenv_values,load_dotenv
import httpx, os, pytz, hashlib, json

"""
    Exécute une requête http vers un serveur avec un calendrier.
"""
def getEventsList(path):
    with httpx.Client() as client:
        response = client.get(path)
        calendar = Calendar(response.text)
    return calendar

"""
    Création d'un hachage de 
    Nom + Jour + Heure de début + Heure de fin + Lieu + Professeur + Année + Direction + Sous-groupe
"""
def createHash(event_icl):
    string = event_icl.name + str(event_icl.day) + str(event_icl.time_start) + str(event_icl.time_end)
    string += ''.join(map(str, event_icl.location))
    string += ''.join(map(str, event_icl.teacher))
    string += ''.join(map(str, event_icl.group))
    string.replace(' ', '')
    string = hashlib.sha256(string.encode()).hexdigest()
    return string

"""
    Créer un objet de event
"""
def createObject(event_icl, odb:OperationDB, lastDetection, event_hash):
    eventObj = Event(
        day = event_icl.day,
        time_start = event_icl.time_start,
        time_end = event_icl.time_end,
        name = event_icl.name,

        last_detection = lastDetection,
        hash = event_hash,
    )

    for location in event_icl.location:
        locObject = Location(name=location)
        eventObj.location.append(odb.create_location(locObject))

    for teacher in event_icl.teacher:
        teacherObject = Teacher(name=teacher)
        eventObj.teacher.append(odb.create_teacher(teacherObject))

    for group in event_icl.group:
        groupObject = GroupTree(name=group)
        eventObj.group.append(odb.create_group(groupObject))

    return eventObj

"""
    Cette fonction crée un hachage puis tente de trouver l'événement à partir de ce hachage
    En cas de succès, elle modifie l'index de la dernière découverte.
    En cas d'échec, elle transmet la recherche ou la création d'objet à la classe de base de données.
"""
def searchEvent(event_icl, odb, lastDetection):
    event_hash = createHash(event_icl)
    eventObj = odb.check_event_existence_hash(event_hash)
    if not eventObj is None:
        eventObj.last_detection = lastDetection
        print("Événement trouvé par hachage")
        return

    eventObj = createObject(event_icl, odb, lastDetection, event_hash)
    print("Создался объект")
    odb.create_event(eventObj) # тут происходит создание нового или дополнение старого объекта

"""
    Introduit de nouveaux champs dans l'événement
"""
def replaceLocationExceptions(event_ics, load):
    location = event_ics.location
    exceptions = load.get("locations", [])
    for key, value in exceptions.items():
        location = location.replace(key, value)
    event_ics.location = location.split("|")

def replaceTeacherExceptions(event_ics, load):
    teachers = event_ics.teacher
    exceptions = load.get("teachers", [])
    for teacher in teachers:
        for key, value in exceptions.items():
            teacher = teacher.replace(key, value)
    event_ics.teacher = teachers

def replaceGroupExceptions(event_ics, load):
    groups = event_ics.group
    exceptions = load.get("groups", [])
    for group in groups:
        for key, value in exceptions.items():
            group = group.replace(key, value)
    event_ics.group = groups


def eventModification(event_ics, load):
    begin = datetime.fromisoformat(str(event_ics.begin)).astimezone(pytz.timezone("Europe/Paris"))
    event_ics.time_end = datetime.fromisoformat(str(event_ics.end)).astimezone(pytz.timezone("Europe/Paris")).time()
    event_ics.day = begin.date()
    event_ics.time_start = begin.time()

    event_ics.description = event_ics.description.split("\n")[2:-2]
    event_ics.group = []
    event_ics.teacher = []

    for ell in event_ics.description:
        if "Parcours" in ell:
            event_ics.group.append(ell.replace("Parcours ", ""))
        elif not any(char.isdigit() for char in ell):
            event_ics.teacher.append(ell)
        elif " " not in ell:
            event_ics.group.append(ell)
        else:
            event_ics.group.append(ell)

    replaceLocationExceptions(event_ics, load)
    replaceTeacherExceptions(event_ics, load)
    replaceGroupExceptions(event_ics, load)


def fullSearch(envEventPath, lastDetection, engine, load):
    with Session(engine) as session:
        with OperationDB(session) as odb:
            c = getEventsList(os.getenv(envEventPath))
            for event in c.events:
                eventModification(event, load)
                searchEvent(event, odb, lastDetection)

def general(engine, lastDetection):
    with open("exceptions.json", "r") as file:
        load = json.load(file)

    configs = dotenv_values()
    for config in configs:
        if config != "DATABASE_URL":
            fullSearch(config, lastDetection, engine, load)