from typing import List, Optional, Literal, Union
from pydantic import BaseModel, Field

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

class MixedItems(BaseModel):
    items: List[Union[Group, Teacher, Location, List[Union[Group, Teacher, Location]]]]

class Event(BaseModel):
    timeStart: str = Field(..., pattern=r"^\d{2}:\d{2}", description="Time start of event in forms: HH:MM")
    timeEnd: str = Field(..., pattern=r"^\d{2}:\d{2}", description="Time end of event in for HH:MM")
    summary: str = Field(..., description="Event summary")
    location: List[str] = Field(..., description="Event location")
    teacher: Optional[List[str]] = Field(None, description="Teacher")
    group: Optional[List[str]] = Field(None, description="Group")

class DaySchedule(BaseModel):
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}",description="Date of day")
    events: List[Event] = Field(..., description="List of events")

class WeekSchedule(BaseModel):
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}", description="Date of first day of week")
    weekSchedule: List[DaySchedule] = Field(..., description="List of week schedule")


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

class SortGroup(BaseModel):
    sort: Optional[Literal["year", "alphabet"]] = None

class SortTeacher(BaseModel):
    sort: Optional[Literal["alphabet"]] = None

class SortLocation(BaseModel):
    sort: Optional[Literal["wing", "alphabet"]] = None