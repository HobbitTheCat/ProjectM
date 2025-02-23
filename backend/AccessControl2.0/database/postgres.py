from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DatabaseURL = os.getenv("DATABASE_URL")
DatabaseAURL = os.getenv("DATABASE_A_URL")

engine = create_async_engine(DatabaseURL, echo=False)
engineA = create_engine(DatabaseAURL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)