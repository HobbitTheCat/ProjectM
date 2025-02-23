from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
from database.databaseFunctions import getDatabase, getFrequentSearch, getLastSearch
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.user import UserCreation, User, MixedItems, InternalUser, UniversalM
from auth.jwtCheck import verify_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/internal/auth/signin")
internalRouter = APIRouter(tags=["internal"])

@internalRouter.post("/api/v1/internal/user")
async def createUser(user: UserCreation, db: AsyncIOMotorDatabase = Depends(getDatabase)):
    name = user.username.replace("_", " ")
    name = name.split("@")[0]
    name = name.title()
    user = User(UID=user.uid, username=user.username, created=datetime.now(), name=name, favorite=[], lastSearched=[], mostSearched=[])
    await db["User"].insert_one(user.model_dump())
    return

@internalRouter.get("/api/v1/internal/user-info", response_model=InternalUser)
async def getUser(token:str =  Depends(oauth2_scheme), db:AsyncIOMotorDatabase = Depends(getDatabase)):
    try:
        payload = verify_jwt_token(token)
        user_id = payload["user_id"]
        user = await db["User"].find_one({"UID": user_id, "active":True})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        mostSearched = [UniversalM.model_validate(item) for item in await getFrequentSearch(user_id, db)]
        lastSearched = [UniversalM.model_validate(item) for item in await getLastSearch(user_id, db)]

        result = InternalUser(name=user["name"],theme=user["theme"],group=user["group"],
                              mostSearched=mostSearched, lastSearched=lastSearched , favorite=user["favorite"])
        return result
    except Exception as e:
        raise e

@internalRouter.delete("/api/v1/internal/user")
async def deleteUser(token:str =  Depends(oauth2_scheme), db:AsyncIOMotorDatabase = Depends(getDatabase)):
    payload = verify_jwt_token(token)
    result = await db["User"].update_one({"UID": payload["user_id"], "active":True}, {"$set": {"active": False}})
    return {"status": "user deleted successfully"}