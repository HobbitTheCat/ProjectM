from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Union
from models.database import Event

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


class SortGroup(BaseModel):
    sort: Optional[Literal["asc", "desc"]] = None
class SortTeacher(BaseModel):
    sort: Optional[Literal["asc","desc"]] = None
class SortLocation(BaseModel):
    sort: Optional[Literal["asc","desc"]] = None

class UniversalM(BaseModel):
    name: str