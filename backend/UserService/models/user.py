import datetime
from pydantic import BaseModel, Field
from typing import List, Union, Literal, Optional


# class Location(BaseModel):
#     location: str
# class Teacher(BaseModel):
#     teacher: str
class Group(BaseModel):
    name: str
# class MixedItems(BaseModel):
#     timestamp: datetime.datetime | None = None
#     id: int | None = None
#     items: Union[Group, Location, Teacher, List[Union[Group, Location, Teacher]]]

class UniversalM(BaseModel):
    name: str
    type: Literal["Teacher","Location","Group"]
class MixedItems(BaseModel):
    items: List[Union[UniversalM, List[UniversalM]]]
    id: Optional[int] = None


class UserCreation(BaseModel):
    uid: int
    username: str


class InternalUser(BaseModel):
    name: str
    theme: bool
    group: str | None = None
    mostSearched: List[UniversalM] | None = None
    lastSearched: List[UniversalM] | None = None
    favorite: List[MixedItems]| None = None

class User(BaseModel):
    UID: int
    username: str
    created: datetime.datetime
    active: bool = True

    name: str
    theme: Literal[0,1] = 0  #0 - light, 1 - dark
    birthday: datetime.date|None = None
    group: str|None = None
    image: str|None = None

    mostSearched: List[UniversalM]
    lastSearched: List[UniversalM]
    favorite: List[MixedItems]
    favoriteIndex: int = 0
