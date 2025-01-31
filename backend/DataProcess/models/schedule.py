from pydantic import BaseModel
from typing import List, Optional, Literal

class Location(BaseModel):
    name:str
    capacity:Optional[int]=None
class Teacher(BaseModel):
    name:str
class Group(BaseModel):
    name:str

class EventResponse(BaseModel):
    day: str
    time_start: str
    time_end: str

    name: str
    location: List[Location]
    teacher: List[Teacher]
    group: List[Group]


class SortGroup(BaseModel):
    sort: Optional[Literal["asc", "desc"]] = None
class SortTeacher(BaseModel):
    sort: Optional[Literal["asc","desc"]] = None
class SortLocation(BaseModel):
    sort: Optional[Literal["asc","desc"]] = None

class UniversalM(BaseModel):
    name: str