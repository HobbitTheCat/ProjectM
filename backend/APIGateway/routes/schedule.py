from fastapi import APIRouter, HTTPException, Depends, Header, status
from models.schedule import *
from auth.token_check import authenticate
from typing import List, Optional, Literal
import httpx
import os

scheduleRouter = APIRouter(
    tags=["schedule"]
)

DATA_PROCESS_URL_WEEK = os.getenv("DataProcessURLWeek")
DATA_PROCESS_URL_DAY = os.getenv("DataProcessURLDay")
DATA_PROCESS_URL_GROUP = os.getenv("DataProcessURLGroup")
DATA_PROCESS_URL_TEACHER = os.getenv("DataProcessURLTeacher")
DATA_PROCESS_URL_LOCATION = os.getenv("DataProcessURLocation")

async def get_schedule(url:str, params: EventRequest, token: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params=params.model_dump(exclude_none=True),
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Failed to connect to downstream service: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@scheduleRouter.get("/api/v1/schedule/week", response_model=List[Event])
async def get_schedules_week(params:EventRequest = Depends(), token: str = Depends(authenticate)):
    return await get_schedule(DataProcessURLWeek, params, token)

@scheduleRouter.get("/api/v1/schedule/day", response_model=List[Event])
async def get_schedules_day(params:EventRequest = Depends(), token: str = Depends(authenticate)):
    return await get_schedule(DataProcessURLDay, params, token)

async def get_lists(url:str, sort:Optional[Literal["year", "alphabet", "wing"]], token: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params={"sort": sort} if sort else {},
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Failed to connect to downstream service: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@scheduleRouter.get("/api/v1/groups", response_model=List[Group])
async def get_list_groups(sort:Optional[Literal["year", "alphabet"]], token: str = Depends(authenticate)):
    return await get_lists(DataProcessURLGroup, sort, token)

@scheduleRouter.get("/api/v1/teachers", response_model=List[Teacher])
async def get_list_teacher(sort:Optional[Literal["alphabet"]], token: str = Depends(authenticate)):
    return await get_lists(DataProcessURLTeacher, sort, token)

@scheduleRouter.get("api/v1/location", response_model=List[Location])
async def get_list_location(sort:Optional[Literal["wing", "alphabet"]], token: str = Depends(authenticate)):
    return await get_lists(DataProcessURLocation, sort, token)