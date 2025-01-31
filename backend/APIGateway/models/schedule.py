from typing import List, Optional, Literal, Union
from pydantic import BaseModel, Field

class Location(BaseModel):
    name: str
    capacity: Optional[int] = None
    class Config:
        schema_extra = {
            "example": {
                "name": "A104",
                "capacity": 100
            }
        }

class Teacher(BaseModel):
    name: str

    class Config:
        schema_extra = {
            "example": {
                "name": "GILLET ANNABELLE"
            }
        }

class Group(BaseModel):
    name: str

    class Config:
        schema_extra = {
            "example": {
                "name": "PC3"
            }
        }

class UniversalM(BaseModel):
    name: str

class MixedItems(BaseModel):
    items: List[Union[Group, Teacher, Location, List[Union[Group, Teacher, Location]]]]

class EventResponse(BaseModel):
    day: str
    time_start: str
    time_end: str

    name: str
    location: List[Location]
    teacher: List[Teacher]
    group: List[Group]


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
    sort: Optional[Literal["asc", "desc"]] = None
class SortTeacher(BaseModel):
    sort: Optional[Literal["asc", "desc"]] = None
class SortLocation(BaseModel):
    sort: Optional[Literal["asc", "desc"]] = None