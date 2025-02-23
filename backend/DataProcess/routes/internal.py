from fastapi import APIRouter, HTTPException
from models.schedule import UniversalM
from models.database import GroupTree, Teacher, Location
from sqlmodel import select
from typing import Type
from database import async_session

internalRouter = APIRouter(tags=["internal"])

async def checkExistence(model: Type, elementName):
    async with async_session() as session:
        query = select(model).where(model.name == elementName)
        result = await session.execute(query)
        item = result.scalars().first()
        return item

@internalRouter.post("/api/v1/internal/check-item", response_model=UniversalM)
async def checkGroupExistence(item: UniversalM):
    model = GroupTree if item.type == "Group" else Teacher if item.type == "Teacher" else Location
    status = await checkExistence(model, item.name)
    if status:
        return UniversalM(name=status.name, type=item.type)
    raise HTTPException(status_code=404, detail="Item not found")

