from http.client import HTTPConnection

from fastapi import APIRouter, Depends, HTTPException, status
import os, httpx
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorDatabase
from database.databaseFunctions import getDatabase, getFrequentSearch, getLastSearch
from models.user import *
from models.update import *
from auth.jwtCheck import verify_jwt_token
from datetime import datetime
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/internal/auth/signin")
userRouter = APIRouter(tags=["user"])

contentCheckURL = os.getenv("DATA_PROCESS_CHECK_URL")
async def checkItemExistence(item: UniversalM):
    async with httpx.AsyncClient() as client:
        result = await client.post(contentCheckURL, json=item.model_dump())
        if result.status_code == 404:
            raise HTTPException(status_code=404, detail="Group not found")
        elif result.status_code != 200:
            raise HTTPException(status_code=500, detail="Internal server error")
        return result

async def updateInfo(user_id:int, field_name:str, value) -> int:
    db = getDatabase()
    updateResult = await db["User"].update_one({"UID": user_id, "active": True}, {"$set":{field_name: value}})
    return updateResult.modified_count


@userRouter.put("/api/v1/internal/user/name")
async def changeName(request: UpdateNameRequest,token:str =  Depends(oauth2_scheme)):
    try:
        payload = verify_jwt_token(token)
        if await updateInfo(payload["user_id"], "name", request.name) > 0:
            return {"status": "success"}
        return {"status": "failed"}
    except HTTPException as e:
        raise e

@userRouter.put("/api/v1/internal/user/birthday")
async def changeBirthday(request: UpdateBirthdayRequest,token:str =  Depends(oauth2_scheme)):
    try:
        payload = verify_jwt_token(token)
        if await updateInfo(payload["user_id"], "birthday", str(request.birthday)) > 0:
            return {"status": "success"}
        return {"status": "fail"}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid date")
    except HTTPException as e:
        raise e

@userRouter.put("/api/v1/internal/user/group")
async def changeGroup(request: Group,token:str =  Depends(oauth2_scheme)):
    try:
        await checkItemExistence(UniversalM(name=request.name, type="Group")) # added existence check
        payload = verify_jwt_token(token)
        if await updateInfo(payload["user_id"], "group", request.name) > 0:
            return {"status": "success"}
        return {"status": "fail"}
    except HTTPException as e:
        raise e

@userRouter.put("/api/v1/internal/user/theme")
async def changeTheme(theme: UpdateThemeRequest,token:str = Depends(oauth2_scheme)):
    try:
        payload = verify_jwt_token(token)
        newTheme = 0 if theme.theme == "light" else 1
        if await updateInfo(payload["user_id"], "theme", newTheme) > 0:
            return {"status": "success"}
        return {"status": "fail"}
    except HTTPException as e:
        raise e

async def get_next_favorite_id(db, userId):
    counter = await db["User"].find_one_and_update(
        {"UID": userId, "active": True},
        {"$inc": {"favoriteIndex": 1}},
        upsert=True,
        return_document=True
    )
    return counter["favoriteIndex"]

@userRouter.post("/api/v1/internal/user/favorite")
async def addFavorite(favorite:MixedItems,token:str =  Depends(oauth2_scheme), db:AsyncIOMotorDatabase = Depends(getDatabase)):
    try:
        for item in favorite.items:
            if isinstance(item, UniversalM):
                await checkItemExistence(item)  # added existence check
            else:
                for i in item:
                    await checkItemExistence(i)
        payload = verify_jwt_token(token)
        favorite_id = await get_next_favorite_id(db, payload["user_id"])
        favorite.id = favorite_id
        await db["User"].update_one({"UID": payload["user_id"], "active":True}, {"$push": {"favorite": favorite.model_dump()}})
        result = await db["User"].find_one({"UID": payload["user_id"], "active": True})
        result = result["favorite"]
        return result
    except httpx.ConnectError:
        print("Connection error")
    except HTTPException as e:
        raise e

@userRouter.post("/api/v1/internal/user/history")
async def addHistory(item: UniversalM, token:str =  Depends(oauth2_scheme), db: AsyncIOMotorDatabase = Depends(getDatabase)):
    try:
        await checkItemExistence(item)
        payload = verify_jwt_token(token)
        itemDict = item.model_dump()
        itemDict["timestamp"] = datetime.now()
        await db["User"].update_one(
            {"UID": payload["user_id"], "active":True},
            {"$push": {"history": {"$each": [itemDict], "$slice": -10}}}
        )
        return {"status": "success"}
    except HTTPException as e:
        raise e

@userRouter.delete("/api/v1/internal/user/favorite")
async def deleteFavorite(index:int, token:str = Depends(oauth2_scheme), db:AsyncIOMotorDatabase = Depends(getDatabase)):
    try:
        payload = verify_jwt_token(token)
        user = await db["User"].find_one({"UID": payload["user_id"], "active":True})
        favorite = user.get("favorite", [])
        new_favorite = [fav for fav in favorite if fav["id"] != index]
        if len(new_favorite) == len(favorite):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        await db["User"].update_one({"UID": payload["user_id"], "active":True}, {"$set": {"favorite": new_favorite}})
        result = await db["User"].find_one({"UID": payload["user_id"], "active": True})
        result = result["favorite"]
        return result
    except HTTPException as e:
        raise e


@userRouter.get("/api/v1/internal/user", response_model=User)
async def getUserInfo(token:str =  Depends(oauth2_scheme), db:AsyncIOMotorDatabase = Depends(getDatabase)):
    try:
        payload = verify_jwt_token(token)
        user_id = payload["user_id"]
        result = await db["User"].find_one({"UID": user_id, "active":True})
        result = User.model_validate(result)
        result.mostSearched = [UniversalM.model_validate(item) for item in await getFrequentSearch(user_id, db)]
        result.lastSearched = [UniversalM.model_validate(item) for item in await getLastSearch(user_id, db)]
        return result
    except HTTPException as e:
        raise e

# @userRouter.get("/api/v1/internal/user/favorite")
# async def getFavorite(token: str = Depends(oauth2_scheme), db:AsyncIOMotorDatabase = Depends(getDatabase)):
#     try:
#         payload = verify_jwt_token(token)
#         result = await db["User"].find_one({"UID": payload["user_id"], "active":True})
#         result = result["favorite"]
#         return result
#     except HTTPException as e:
#         raise e