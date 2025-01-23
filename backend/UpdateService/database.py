from sqlmodel import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
DataBaseURL = os.getenv("DATABASE_URL")

engine = create_engine(DataBaseURL, echo=True)
