from typing import List, Optional
from pydantic import BaseModel

class Location(BaseModel):
    location: str

    class Config:
        schema_extra = {
            "example": {
                "location": "A104"
            }
        }

class Teacher(BaseModel):
    teacher: str

    class Config:
        schema_extra = {
            "example": {
                "teacher": "GILLET ANNABELLE"
            }
        }

class Group(BaseModel):
    group: str

    class Config:
        schema_extra = {
            "example": {
                "group": "PC3"
            }
        }

class Event(BaseModel):
    date: str
    timeStart: str
    timeEnd: str

    summary: str
    location: List[str]
    teacher: Optional[List[str]] = None
    group: Optional[List[str]] = None

    class Config:
        schema_extra = {
            "examples": {
                "date":"2025-01-08",
                "timeStart":"08:00",
                "timeEnd":"10:00",
                "summary": "Phys3B",
                "location": ["A104", "A105"],
                "teacher": ["GILLET ANNABELLE"],
                "group": ["PC3"]
            }
        }

class EventRequest(BaseModel):
    date: str
    location: Optional[List[str]] = None
    teacher: Optional[List[str]] = None
    group: Optional[List[str]] = None

    class Config:
        schema_extra = {
            "examples": {
                "date":"2025-01-08",
                "summary": "Phys3B",
                "location": ["A104", "A105"],
                "teacher": ["GILLET ANNABELLE"],
                "group": ["PC3"]
            }
        }