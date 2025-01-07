from fastapi import APIRouter, Depends
import json
from token_check import authenticate
from models import *

mockRouter = APIRouter(tags=["routes"])

# user: str = Depends(authenticate)

@mockRouter.get("/api/v1/internal/event/week", response_model=WeekSchedule)
async def get_schedule_week(params:EventRequest = Depends(), user: str = Depends(authenticate)):
    with open("testData.json") as f:
        data = json.load(f)
    return data.get("week_schedule", [])

@mockRouter.get("/api/v1/internal/event/day", response_model=DaySchedule)
async def get_schedule_day(params:EventRequest = Depends(), user: str = Depends(authenticate)):
    with open("testData.json") as f:
        data = json.load(f)
    return data.get("day_schedule", [])

@mockRouter.get("/api/v1/internal/event/group-list", response_model=List[Group])
async def get_schedule_groups(sort: SortGroup = Depends(), user: str = Depends(authenticate)):
    with open("testData.json") as f:
        data = json.load(f)
    return data.get("group_list", [])

@mockRouter.get("/api/v1/internal/event/location-list", response_model=List[Location])
async def get_schedule_location(sort:SortLocation = Depends(), user: str = Depends(authenticate)):
    with open("testData.json") as f:
        data = json.load(f)
    return data.get("location_list", [])

@mockRouter.get("/api/v1/internal/event/teacher-list", response_model=List[Teacher])
async def get_schedule_teacher(sort:SortTeacher = Depends(), user: str = Depends(authenticate)):
    with open("testData.json") as f:
        data = json.load(f)
    return data.get("teacher_list", [])


@mockRouter.get("/api/v1/internal/user/favorite-list", response_model=MixedItems)
async def get_user_favorites(user: str = Depends(authenticate)):
    with open("testData.json") as f:
        data = json.load(f)
    return data.get("favorite_list", [])

@mockRouter.get("/api/v1/internal/user/history-list", response_model=MixedItems)
async def get_user_history(user: str = Depends(authenticate)):
    with open("testData.json") as f:
        data = json.load(f)
    return data.get("last_searched", [])


@mockRouter.post("/api/v1/internal/user/history")
async def post_user_history(items: MixedItems,  user: str = Depends(authenticate)):
    return {"status": "History added successfully"}

@mockRouter.post("/api/v1/internal/user/favorite")
async def post_user_favorite(items: MixedItems,  user: str = Depends(authenticate)):
    return {"status": "Favorite added successfully"}