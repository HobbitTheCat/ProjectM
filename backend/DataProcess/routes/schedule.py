from itertools import chain
from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlmodel import select
from sqlalchemy.orm import selectinload
from fastapi.security import OAuth2PasswordBearer
from database import async_session
from models.schedule import EventResponse
from models.schedule import SortGroup, SortLocation, SortTeacher, SortItems
from models.schedule import UniversalM
from models.database import *
from datetime import datetime, timedelta
from typing import List, Optional, Type
from auth.token_check import verify_jwt_token
from routes.internal import checkExistence

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/internal/auth/signin")

scheduleRouter = APIRouter(tags=["schedule"])

def reformatData(data):
    result = []
    for item in data:
        dump = item.model_dump(exclude={"id", "hash", "last_detection"})
        dump["day"] = item.day.strftime("%Y-%m-%d")
        dump["time_start"] = item.time_start.strftime("%H:%M")
        dump["time_end"] = item.time_end.strftime("%H:%M")

        # dump.update({"location": [loc.model_dump(exclude={"id"}) for loc in item.location]})
        # dump.update({"teacher": [tea.model_dump(exclude={"id", "location_id"}) for tea in item.teacher]})
        # dump.update({"group": [gr.model_dump(exclude={"id", "parent_id"}) for gr in item.group]})
        dump.update({"location": [UniversalM(name=loc.name, type="Location") for loc in item.location]}) # возможно это не будет работать
        dump.update({"teacher": [UniversalM(name=tea.name, type="Teacher") for tea in item.teacher]})
        dump.update({"group": [UniversalM(name=gr.name, type="Group") for gr in item.group]})

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

def checkItemExistence(location=None, group=None, teacher=None):
    if not location is None:
        for l in location:
            if checkExistence(Location, l) is None:
                raise HTTPException(status_code=404, detail="Location not found")
    if not group is None:
        for g in group:
            if checkExistence(GroupTree, g) is None:
                raise HTTPException(status_code=404, detail="Group not found")
    if not teacher is None:
        for t in teacher:
            if checkExistence(Teacher, t) is None:
                raise HTTPException(status_code=404, detail="Teacher not found")

@scheduleRouter.get("/api/v1/internal/event/day", response_model=List[EventResponse])
async def get_schedule_day(date: str,
                           location: Optional[List[str]] = Query(None),
                           group: Optional[List[str]] = Query(None),
                           teacher: Optional[List[str]] = Query(None),token:str =  Depends(oauth2_scheme)):
    verify_jwt_token(token)
    checkItemExistence(location, group, teacher)
    try:
        targetDate = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid date")
    return await getDaySchedule([targetDate], location, group, teacher)


@scheduleRouter.get("/api/v1/internal/event/week", response_model=List[EventResponse])
async def get_schedule_week(date: str,
                            location: Optional[List[str]] = Query(None),
                            group: Optional[List[str]] = Query(None),
                            teacher: Optional[List[str]] = Query(None),token:str =  Depends(oauth2_scheme)):
    verify_jwt_token(token)
    checkItemExistence(location, group, teacher)
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid date")
    monday = date - timedelta(date.weekday())
    weekDate = [monday + timedelta(days=i) for i in range(7)]
    return await getDaySchedule(weekDate, location, group, teacher)


async def getInfoList(model:Type, sort:str):
    try:
        async with async_session() as session:
            query = select(model)
            if sort == "asc":
                query = query.order_by(model.name)
            elif sort == "desc":
                query = query.order_by(model.name.desc())
            result = await session.execute(query)
            items = result.scalars().all()
            if model == GroupTree:
                return [UniversalM(name=item.name, type="Group") for item in items]
            return [UniversalM(name=item.name, type=model.__name__) for item in items]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def getItemByStart(model: Type, start: str):
    try:
        async with async_session() as session:
            query = select(model).where(model.name.ilike(f"%{start}%"))
            result = await session.execute(query)
            items = result.scalars().all()
            return [UniversalM(name=item.name, type=model.__name__) for item in items]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@scheduleRouter.get("/api/v1/internal/event/location-list", response_model=List[UniversalM])
async def get_schedule_location(sort:SortLocation = Depends(),token:str =  Depends(oauth2_scheme)):
    verify_jwt_token(token)
    return await getInfoList(Location, sort.sort)

@scheduleRouter.get("/api/v1/internal/event/teacher-list", response_model=List[UniversalM])
async def get_schedule_teacher(sort:SortTeacher = Depends(),token:str =  Depends(oauth2_scheme)):
    verify_jwt_token(token)
    return await getInfoList(Teacher, sort.sort)

@scheduleRouter.get("/api/v1/internal/event/group-list", response_model=List[UniversalM])
async def get_groups(sort: SortGroup = Depends(),token:str =  Depends(oauth2_scheme)):
    verify_jwt_token(token)
    return await getInfoList(GroupTree, sort.sort)

# token:str =  Depends(oauth2_scheme)
@scheduleRouter.get("/api/v1/internal/event/item-list", response_model=List[UniversalM])
async def ger_items(start: str,
                    sort: SortItems = Depends(), token:str =  Depends(oauth2_scheme)):
    verify_jwt_token(token)
    sort = sort.sort if sort is not None else None
    arrOfItems = list(chain(await getItemByStart(Location, start), await getItemByStart(Teacher, start),await getItemByStart(GroupTree, start)))
    if len(arrOfItems) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items found")
    if sort == "asc":
        arrOfItems = sorted(arrOfItems, key=lambda item: item.name)
    elif sort == "desc":
        arrOfItems = sorted(arrOfItems, reverse=True, key=lambda item: item.name)
    return arrOfItems
