import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv

load_dotenv()
mogoURL = os.getenv("MONGO_URL")
client = AsyncIOMotorClient(mogoURL)
database = client["User"]
collection = database["Users"]

def getDatabase() -> AsyncIOMotorDatabase:
    return database

async def getFrequentSearch(user_id: int, db:AsyncIOMotorDatabase):
    pipeline = [
    {"$match": {"UID": user_id, "active": True}},
    {"$unwind": "$history"},
    {"$group": {
        "_id": {
            "name": "$history.name",
            "type": "$history.type"
        },
        "count": {"$sum": 1}
    }},
    {"$sort": {"count": -1}},
    {"$limit": 2}
]
    result = await db["User"].aggregate(pipeline).to_list(length=2)
    return [item["_id"] for item in result] if result else []

async def getLastSearch(user_id: int, db:AsyncIOMotorDatabase):
    user_data = await db["User"].find_one(
        {"UID": user_id, "active": True},
        {"history": {"$slice": -2}}
    )
    if user_data and "history" in user_data and user_data["history"]:
        return user_data["history"]
    return []