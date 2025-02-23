from database.databaseFunctions import getDatabase
from datetime import datetime
from auth.jwtCheck import verify_jwt_token
from models.user import UserCreation, User, MixedItems, UniversalM
from models.update import UpdateBirthdayRequest
import asyncio

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo1MjU2MDAsInVzZXJfaWQiOjEsInJlZnJlc2giOmZhbHNlLCJleHAiOjE3Mzk0NjUwMTZ9.MtNUdHz3JKpxfX7NV5fzvQaRMdHj68wZopyGsvv3_h8"

async def example(user: UserCreation):
    db = getDatabase()
    payload = verify_jwt_token(token)
    name = user.username.replace("_", " ")
    name = name.split("@")[0]
    name = name.title()
    user = User(UID=payload["user_id"], username=user.username, created=user.created, name=name, favorite=[], lastSearched=[])
    await db["User"].insert_one(user.model_dump())

async def read():
    db = getDatabase()

    payload = verify_jwt_token(token)
    result = await db["User"].find_one({"UID": payload["user_id"], "active": True})
    print(result)
    result = User.model_validate(result)
    return result

async def changeBirthday(request: UpdateBirthdayRequest):
    try:
        payload = verify_jwt_token(token)
        if await updateInfo(payload["user_id"], "birthday", str(request.birthday)) > 0:
            return {"status": "success"}
        return {"status": "fail"}
    except Exception as e:
        raise e

async def addFavorite(favorite:MixedItems):
    db = getDatabase()
    try:
        payload = verify_jwt_token(token)
        update_result = await db["User"].update_one({"UID": payload["user_id"], "active":True}, {"$push": {"favorite": favorite.model_dump()}})
        if update_result.modified_count > 0:
            return {"status": "success"}
        return {"status": "fail"}
    except Exception as e:
        raise e

from routes.user import getUserInfo
from database.databaseFunctions import getLastSearch, getFrequentSearch

async def getHistory():
    db = getDatabase()
    history = await getLastSearch(1, db)
    history = [UniversalM.model_validate(item) for item in history]
    return history

async def getMostSearched():
    db = getDatabase()
    return await getFrequentSearch(1, db)

async def getUserI():
    db = getDatabase()
    # return await getUserInfo(token, db)
    return await db["User"].find_one({"UID": 1, "active":True})


from routes.user import updateInfo
async def changeName():
    await updateInfo(1, "name", "Denis")

# print(asyncio.run(getMostSearched()))
# print(asyncio.run(getHistory()))
print(asyncio.run(getUserI()))