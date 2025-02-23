from fastapi import APIRouter, HTTPException
from models.schedule import UniversalM
from models.database import GroupTree, Teacher, Location
from sqlmodel import select
from typing import Type
from database import async_session
import asyncio

async def checkExistence(model: Type, elementName):
    async with async_session() as session:
        query = select(model).where(model.name == elementName)
        result = await session.execute(query)
        item = result.scalars().first()
        return item

print(asyncio.run(checkExistence(GroupTree, "MI4-FC")))