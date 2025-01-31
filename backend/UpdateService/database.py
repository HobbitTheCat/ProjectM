from sqlmodel import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
DataBaseURL = os.getenv("DATABASE_URL")
DataBaseURLA = os.getenv("DATABASE_URL_A")

engine = create_engine(DataBaseURL, echo=False)
engineA = create_engine(DataBaseURLA, echo=False)