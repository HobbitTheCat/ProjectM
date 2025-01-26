from routes.schedule import getDaySchedule
from typing import List, Type
import asyncio, os
from dotenv import load_dotenv
from sqlmodel import create_engine,Session, select
from models.schedule import  EventRequest
from models.database import *
from datetime import datetime

# model = EventRequest(date="2025-01-24", subgroup=["MI4-FC"])
# targetDate = datetime.strptime(model.date, "%Y-%m-%d").date()
# print(asyncio.run(getDaySchedule(targetDate, model)))

load_dotenv()
DataBaseURL = os.getenv("DATABASE_URL_NOTAS")
engine = create_engine(DataBaseURL)

def reformatData(data):
    result = []
    for item in data:
        dump = item.model_dump(exclude={"id", "hash", "last_detection"})
        dump["day"] = item.day.strftime("%Y-%m-%d")
        dump["time_start"] = item.time_start.strftime("%H:%M")
        dump["time_end"] = item.time_end.strftime("%H:%M")

        dump.update({"location": [loc.model_dump(exclude={"id"}) for loc in item.location]})
        dump.update({"teacher": [tea.model_dump(exclude={"id", "location_id"}) for tea in item.teacher]})
        dump.update({"group": [gr.model_dump(exclude={"id", "parent_id"}) for gr in item.group]})

        result.append(dump)
    return result

def getGroupDown(session, groupId: int, exitList = None):
    if exitList is None:
        exitList = []
    subgroupList = session.exec(select(GroupTree).where(GroupTree.parent_id==groupId)).all()
    exitList.extend(subgroupList)
    for subgroup in subgroupList:
        exitList.extend(getGroupDown(session, subgroup.id, exitList))
    return exitList

def getGroupUp(session, groupId: int, exitList = None):
    if exitList is None:
        exitList = []
    parent = session.exec(select(GroupTree).where(GroupTree.id==groupId)).first()
    exitList.append(parent)
    if parent.parent_id is None:
        return exitList
    return getGroupUp(session, parent.parent_id, exitList)

def get_schedule_day(params, targetDate):
    with Session(engine) as session:
        query = select(Event).where(Event.day == targetDate)
        if params.location:
            query = query.join(EventLocation).join(Location).where(Location.name.in_(params.location))
        if params.teacher:
            query = query.join(EventTeacher).join(Teacher).where(Teacher.name.in_(params.teacher))
        if params.group:
            subQuery = select(GroupTree).where(GroupTree.name.in_(params.group))
            groupList = session.exec(subQuery).all()
            additionalGroups = params.group
            for group in groupList:
                additionalGroups.extend([item.name for item in getGroupUp(session, group.id) if item.name not in additionalGroups])
                additionalGroups.extend([item.name for item in getGroupDown(session, group.id) if item.name not in additionalGroups])
            query = query.join(EventGroup).join(GroupTree).where(GroupTree.name.in_(additionalGroups))

        events = reformatData(session.exec(query).all())
        return events


model = EventRequest(date="2025-01-28", teacher=["BAILLEUX OLIVIER"])
date = datetime.strptime(model.date, "%Y-%m-%d").date()
result = get_schedule_day(model, date)
for i in result:
    print(i)