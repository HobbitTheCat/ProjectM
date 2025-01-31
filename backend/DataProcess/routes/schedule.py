from http.client import HTTPException
from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlmodel import select
from sqlalchemy.orm import selectinload
from database import async_session
from auth.token_check import authenticate
from models.schedule import EventResponse
from models.schedule import SortGroup, SortLocation, SortTeacher
from models.schedule import UniversalM
from models.database import *
from datetime import datetime, timedelta
from typing import List, Optional, Type

scheduleRouter = APIRouter(tags=["schedule"])
# , user: str = Depends(authenticate)

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

async def getGroupDown(session, groupId: int, exitList = None):
    if exitList is None:
        exitList = []
    subgroupList = await session.execute(select(GroupTree).where(GroupTree.parent_id==groupId))
    subgroupList = subgroupList.scalars().all()
    exitList.extend(subgroupList)
    for subgroup in subgroupList:
        exitList.extend(await getGroupDown(session, subgroup.id, exitList))
    return exitList

async def getGroupUp(session, groupId: int, exitList = None):
    if exitList is None:
        exitList = []
    parent = await session.execute(select(GroupTree).where(GroupTree.id==groupId))
    parent = parent.scalars().first()
    exitList.append(parent)
    if parent.parent_id is None:
        return exitList
    return await getGroupUp(session, parent.parent_id, exitList)

async def getDaySchedule(date, location_list, group_list, teacher_list):
    try:
        async with async_session() as session:
            query  = select(Event).where(Event.day.in_(date))
            if location_list:
                query = query.join(EventLocation).join(Location).where(Location.name.in_(location_list))
            if teacher_list:
                query = query.join(EventTeacher).join(Teacher).where(Teacher.name.in_(teacher_list))
            if group_list:
                subQuery = select(GroupTree).where(GroupTree.name.in_(group_list))
                groupList = await session.execute(subQuery)
                groupList = groupList.scalars().all()
                additionalGroups = group_list
                for group in groupList:
                    groupUp = await getGroupUp(session, group.id)
                    additionalGroups.extend([item.name for item in groupUp if item.name not in additionalGroups])
                    groupDown = await getGroupDown(session, group.id)
                    additionalGroups.extend([item.name for item in groupDown if item.name not in additionalGroups])
                query = query.join(EventGroup).join(GroupTree).where(GroupTree.name.in_(additionalGroups))

            query = query.options(
                selectinload(Event.location),
                selectinload(Event.teacher),
                selectinload(Event.group)
            )

            result = await session.execute(query)
            events = result.scalars().all()
            events = reformatData(events)

            return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# , user: str = Depends(authenticate)
@scheduleRouter.get("/api/v1/internal/event/day", response_model=List[EventResponse])
async def get_schedule_day(date: str,
                           location: Optional[List[str]] = Query(None),
                           group: Optional[List[str]] = Query(None),
                           teacher: Optional[List[str]] = Query(None), user: str = Depends(authenticate)):
    try:
        targetDate = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid date")
    return await getDaySchedule([targetDate], location, group, teacher)


@scheduleRouter.get("/api/v1/internal/event/week", response_model=List[EventResponse])
async def get_schedule_week(date: str,
                            location: Optional[List[str]] = Query(None),
                            group: Optional[List[str]] = Query(None),
                            teacher: Optional[List[str]] = Query(None), user: str = Depends(authenticate)):
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid date")
    monday = date - timedelta(date.weekday())
    weekDate = [monday + timedelta(days=i) for i in range(7)]
    return await getDaySchedule(weekDate, location, group, teacher)


async def getInfoList(model:Type, sort:str, excludedFields:set = {"id"}):
    try:
        async with async_session() as session:
            query = select(model)
            if sort == "asc":
                query = query.order_by(model.name)
            elif sort == "desc":
                query = query.order_by(model.name.desc())
            result = await session.execute(query)
            items = result.scalars().all()
            result = [item.model_dump(exclude=excludedFields) for item in items]
            return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@scheduleRouter.get("/api/v1/internal/event/location-list", response_model=List[UniversalM])
async def get_schedule_location(sort:SortLocation = Depends(), user: str = Depends(authenticate)):
    sort = sort.sort
    return await getInfoList(Location, sort)

@scheduleRouter.get("/api/v1/internal/event/teacher-list", response_model=List[UniversalM])
async def get_schedule_teacher(sort:SortTeacher = Depends(), user: str = Depends(authenticate)):
    sort = sort.sort
    return await getInfoList(Teacher, sort, {"id", "location_id"})

@scheduleRouter.get("/api/v1/internal/event/group-list", response_model=List[UniversalM])
async def get_groups(sort: SortGroup = Depends(), user: str = Depends(authenticate)):
    sort = sort.sort
    return await getInfoList(GroupTree, sort, {"id", "parent_id"})
