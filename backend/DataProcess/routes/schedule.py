from http.client import HTTPException
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import select
from sqlalchemy.orm import selectinload
from typing import List, Type
from database import async_session
from auth.token_check import authenticate
from models.schedule import EventRequest, WeekSchedule, DaySchedule
from models.schedule import SortGroup, SortLocation, SortTeacher
from models.schedule import UniversalM
from models.database import *
from datetime import datetime

scheduleRouter = APIRouter(tags=["schedule"])
# , user: str = Depends(authenticate)

async def getDaySchedule(date, params):
    try:
        async with async_session() as session:
            query  = select(Event).where(Event.day == date)
            if params.location:
                query = query.join(EventLocation).join(Location).where(Location.name.in_(params.location))
            if params.teacher:
                query = query.join(EventTeacher).join(Teacher).where(Teacher.name.in_(params.teacher))
            if params.direction:
                query = query.join(EventDirection).join(Direction).where(Direction.name.in_(params.direction))
            if params.subgroup:
                query = query.join(EventSubgroup).join(Subgroup).where(Subgroup.name.in_(params.subgroup))

            query = query.options(
                selectinload(Event.location),
                selectinload(Event.teacher),
                selectinload(Event.year),
                selectinload(Event.direction),
                selectinload(Event.subgroup),
            )

            result = await session.execute(query)
            events = result.scalars().all()

            result = []
            for event in events:
                dump = event.model_dump(exclude={"id", "hash", "last_detection"})
                dump["day"] = event.day.strftime("%Y-%m-%d")
                dump["time_start"] = event.time_start.strftime("%H:%M")
                dump["time_end"] = event.time_end.strftime("%H:%M")

                dump.update({"location": [loc.model_dump(exclude={"id"}) for loc in event.location]})
                dump.update({"teacher": [tea.model_dump(exclude={"id", "location_id"}) for tea in event.teacher]})
                dump.update({"year": [yea.model_dump(exclude={"id"}) for yea in event.year]})
                dump.update({"direction": [direct.model_dump(exclude={"id", "year_id"}) for direct in event.direction]})
                dump.update({"subgroup": [sub.model_dump(exclude={"id", "direction_id"}) for sub in event.subgroup]})
                result.append(dump)

            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@scheduleRouter.get("/api/v1/internal/event/week", response_model=WeekSchedule)
async def get_schedule_week(params:EventRequest = Depends()):
    ...
@scheduleRouter.get("/api/v1/internal/event/day", response_model=DaySchedule)
async def get_schedule_day(params:EventRequest = Depends()):
    targetDate = datetime.strptime(params.date, "%Y-%m-%d").date()
    return await getDaySchedule(targetDate, params)


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
async def get_schedule_location(sort:SortLocation = Depends()):
    sort = sort.sort
    return await getInfoList(Location, sort)

@scheduleRouter.get("/api/v1/internal/event/teacher-list", response_model=List[UniversalM])
async def get_schedule_teacher(sort:SortTeacher = Depends()):
    sort = sort.sort
    return await getInfoList(Teacher, sort, {"id", "location_id"})

@scheduleRouter.get("/api/v1/internal/event/group-list", response_model=List[UniversalM])
async def get_groups(sort: SortGroup = Depends()):
    sort = sort.sort
    return await getInfoList(GroupTree, sort, {"id", "parent_id"})
