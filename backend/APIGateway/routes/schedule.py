from fastapi import APIRouter, HTTPException, Depends, status, Query
from models.schedule import *
from auth.token_check import authenticate
from typing import List
import httpx, os
from dotenv import load_dotenv

load_dotenv()

scheduleRouter = APIRouter(
    tags=["schedule"]
)

DataProcessURLWeek = os.getenv("DATA_PROCESS_URL_WEEK")
DataProcessURLDay = os.getenv("DATA_PROCESS_URL_DAY")
DataProcessURLGroup = os.getenv("DATA_PROCESS_URL_GROUP")
DataProcessURLTeacher = os.getenv("DATA_PROCESS_URL_TEACHER")
DataProcessURLocation = os.getenv("DATA_PROCESS_URL_LOCATION")

async def get_info(url:str, params, token: str): # =Depends() под вопросом
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
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                                detail=f"Failed to connect to downstream service: {e}")
    except httpx.HTTPStatusError as e:
        try:
            errorDetail = e.response.json().get("detail", e.response.text)
        except ValueError:
            errorDetail = e.response.text
        raise HTTPException(status_code=e.response.status_code, detail=errorDetail)

#
@scheduleRouter.get("/api/v1/schedule/week", response_model=List[EventResponse])
async def get_schedules_week(date:str,
                             location:Optional[List[str]] = Query(None),
                             group:Optional[List[str]] = Query(None),
                             teacher:Optional[List[str]] = Query(None),
                             token: str = Depends(authenticate)):
    model = EventRequest(date=date,location=location,group=group,teacher=teacher)
    return await get_info(DataProcessURLWeek, model, token)

@scheduleRouter.get("/api/v1/schedule/day", response_model=List[EventResponse])
async def get_schedules_day(date:str,
                            location:Optional[List[str]] = Query(None),
                            group:Optional[List[str]] = Query(None),
                            teacher:Optional[List[str]] = Query(None),
                            token: str = Depends(authenticate)):
    model = EventRequest(date=date,location=location,group=group,teacher=teacher)
    return await get_info(DataProcessURLDay, model, token)



@scheduleRouter.get("/api/v1/group-list", response_model=List[UniversalM])
async def get_list_groups(sort:SortGroup = Depends(), token: str = Depends(authenticate)):
    return await get_info(DataProcessURLGroup, sort, token)

@scheduleRouter.get("/api/v1/teacher-list", response_model=List[UniversalM])
async def get_list_teacher(sort:SortTeacher = Depends(), token: str = Depends(authenticate)):
    return await get_info(DataProcessURLTeacher, sort, token)

@scheduleRouter.get("/api/v1/location-list", response_model=List[UniversalM])
async def get_list_location(sort:SortLocation = Depends(), token: str = Depends(authenticate)):
    return await get_info(DataProcessURLocation, sort, token)