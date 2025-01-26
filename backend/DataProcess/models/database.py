import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class EventTeacher(SQLModel, table=True):
    event_id: int | None = Field(default=None, foreign_key="event.id" ,primary_key=True)
    teacher_id: int | None = Field(default=None, foreign_key="teacher.id", primary_key=True)

class EventLocation(SQLModel, table=True):
    event_id: int | None = Field(default=None, foreign_key="event.id", primary_key=True)
    location_id: int | None = Field(default=None, foreign_key="location.id", primary_key=True)

class EventGroup(SQLModel, table=True):
    event_id: int | None = Field(default=None, foreign_key="event.id", primary_key=True)
    group_id: int | None = Field(default=None, foreign_key="grouptree.id", primary_key=True)

class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    day: datetime.date = Field(index=True)
    time_start: datetime.time
    time_end: datetime.time
    name: str

    hash: str = Field(index=True)
    last_detection: int 

    location: list["Location"] = Relationship(back_populates="events", link_model=EventLocation)
    teacher: list["Teacher"] = Relationship(back_populates="events", link_model=EventTeacher)
    group: list["GroupTree"] = Relationship(back_populates="events", link_model=EventGroup)

class Location(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    capacity: int | None = Field(default=None)

    events: list[Event] = Relationship(back_populates="location", link_model=EventLocation)

class Teacher(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str= Field(unique=True)
    location_id: int | None = Field(default=None, foreign_key="location.id")

    events: list[Event] = Relationship(back_populates="teacher", link_model=EventTeacher)

class GroupTree(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    parent_id: int | None = Field(default=None, foreign_key="grouptree.id")
    name: str

    parent: Optional["GroupTree"] = Relationship(back_populates="children", sa_relationship_kwargs={"remote_side": "GroupTree.id"})
    children: list["GroupTree"] = Relationship(back_populates="parent")
    events: list[Event] = Relationship(back_populates="group", link_model=EventGroup)
