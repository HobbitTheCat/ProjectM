from routes.schedule import getDaySchedule, get_schedule_day
from typing import List, Type
import asyncio, os
from dotenv import load_dotenv
from sqlmodel import create_engine,Session, select
from models.database import *
from datetime import datetime, timedelta

# print(asyncio.run(get_schedule_day(date="2025-01-27",group=["IE4-I42"])))

# date = "2025-01-27"
# date = datetime.strptime(date, "%Y-%m-%d")
# monday = date - timedelta(date.weekday())
# weekDate = [(monday + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
# bigSchedule = []
# for day in weekDate:
#     targetDate = datetime.strptime(day, "%Y-%m-%d").date()
#     bigSchedule.extend(asyncio.run(getDaySchedule(targetDate, None, ["MI4-FC"], None)))
# print(weekDate)

date = ["2025-01-27", "2025-01-28"]
bigSchedule = []
for date in date:
    targetDate = datetime.strptime(date, "%Y-%m-%d").date()
    result = asyncio.run(getDaySchedule(targetDate, None, ["MI4-FC"], None))
    bigSchedule.extend(result)
print(bigSchedule)

# load_dotenv()
# DataBaseURL = os.getenv("DATABASE_URL_NOTAS")
# engine = create_engine(DataBaseURL)
#
# def reformatData(data):
#     result = []
#     for item in data:
#         dump = item.model_dump(exclude={"id", "hash", "last_detection"})
#         dump["day"] = item.day.strftime("%Y-%m-%d")
#         dump["time_start"] = item.time_start.strftime("%H:%M")
#         dump["time_end"] = item.time_end.strftime("%H:%M")
#
#         dump.update({"location": [loc.model_dump(exclude={"id"}) for loc in item.location]})
#         dump.update({"teacher": [tea.model_dump(exclude={"id", "location_id"}) for tea in item.teacher]})
#         dump.update({"group": [gr.model_dump(exclude={"id", "parent_id"}) for gr in item.group]})
#
#         result.append(dump)
#     return result
#
# def getGroupDown(session, groupId: int, exitList = None):
#     if exitList is None:
#         exitList = []
#     subgroupList = session.exec(select(GroupTree).where(GroupTree.parent_id==groupId)).all()
#     exitList.extend(subgroupList)
#     for subgroup in subgroupList:
#         exitList.extend(getGroupDown(session, subgroup.id, exitList))
#     return exitList
#
# def getGroupUp(session, groupId: int, exitList = None):
#     if exitList is None:
#         exitList = []
#     parent = session.exec(select(GroupTree).where(GroupTree.id==groupId)).first()
#     exitList.append(parent)
#     if parent.parent_id is None:
#         return exitList
#     return getGroupUp(session, parent.parent_id, exitList)
#
# def get_schedule_day(params, targetDate):
#     with Session(engine) as session:
#         query = select(Event).where(Event.day == targetDate)
#         if params.location:
#             query = query.join(EventLocation).join(Location).where(Location.name.in_(params.location))
#         if params.teacher:
#             query = query.join(EventTeacher).join(Teacher).where(Teacher.name.in_(params.teacher))
#         if params.group:
#             subQuery = select(GroupTree).where(GroupTree.name.in_(params.group))
#             groupList = session.exec(subQuery).all()
#             additionalGroups = params.group
#             for group in groupList:
#                 additionalGroups.extend([item.name for item in getGroupUp(session, group.id) if item.name not in additionalGroups])
#                 additionalGroups.extend([item.name for item in getGroupDown(session, group.id) if item.name not in additionalGroups])
#             query = query.join(EventGroup).join(GroupTree).where(GroupTree.name.in_(additionalGroups))
#
#         events = reformatData(session.exec(query).all())
#         return events
#
#
# model = EventRequest(date="2025-01-28", teacher=["BAILLEUX OLIVIER"])
# date = datetime.strptime(model.date, "%Y-%m-%d").date()
# result = get_schedule_day(model, date)
# for i in result:
#     print(i)