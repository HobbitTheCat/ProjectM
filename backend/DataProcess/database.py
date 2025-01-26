from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DataBaseURL = os.getenv("DATABASE_URL")

engine = create_async_engine(DataBaseURL, echo=False)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)