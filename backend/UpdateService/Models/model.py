import datetime
from dataclasses import field
from wsgiref.validate import validator
from pydantic import field_validator
from sqlalchemy import True_

from sqlmodel import Field, SQLModel, Relationship

class EventTeacher(SQLModel, table=True):
    event_id: int | None = Field(default=None, foreign_key="event.id" ,primary_key=True)
    teacher_id: int | None = Field(default=None, foreign_key="teacher.id", primary_key=True)

class EventLocation(SQLModel, table=True):
    event_id: int | None = Field(default=None, foreign_key="event.id", primary_key=True)
    location_id: int | None = Field(default=None, foreign_key="location.id", primary_key=True)

class EventYear(SQLModel, table=True):
    event_id: int | None = Field(default=None, foreign_key="event.id", primary_key=True)
    year_id: int | None = Field(default=None, foreign_key="year.id", primary_key=True)

class EventDirection(SQLModel, table=True):
    event_id: int | None = Field(default=None, foreign_key="event.id", primary_key=True)
    direction_id: int | None = Field(default=None, foreign_key="direction.id", primary_key=True)

class EventSubgroup(SQLModel, table=True):
    event_id: int | None = Field(default=None, foreign_key="event.id", primary_key=True)
    subgroup_id: int | None = Field(default=None, foreign_key="subgroup.id", primary_key=True)

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
    year: list["Year"] = Relationship(back_populates="events", link_model=EventYear)
    direction: list["Direction"] = Relationship(back_populates="events", link_model=EventDirection)
    subgroup: list["Subgroup"] = Relationship(back_populates="events", link_model=EventSubgroup)

    def add(self, other: "Event"):
        selfDict = self.model_dump(exclude={"id", "day", "time_start", "time_end", "name"})
        otherDict = other.model_dump(exclude={"id", "day", "time_start", "time_end", "name"})
        print(selfDict)
        print(otherDict)

        for key, value in otherDict.items():
            if key in selfDict:
                selfDict[key].extend(item for item in value if item not in selfDict[key])
            else:
                selfDict[key] = value.copy()

        return self



class Location(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    capacity: int | None = Field(default=None)

    events: list[Event] = Relationship(back_populates="location", link_model=EventLocation)

class Teacher(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    location_id: int | None = Field(default=None, foreign_key="location.id")

    events: list[Event] = Relationship(back_populates="teacher", link_model=EventTeacher)

class Year(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    events: list[Event] = Relationship(back_populates="year", link_model=EventYear)
    directions: list["Direction"] = Relationship(back_populates="year")

class Direction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    year_id: int = Field(foreign_key="year.id")

    events: list[Event] = Relationship(back_populates="direction", link_model=EventDirection)
    year: Year = Relationship(back_populates="directions")
    subgroups: list["Subgroup"] = Relationship(back_populates="direction")

class Subgroup(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    direction_id: int = Field(foreign_key="direction.id")

    events: list[Event] = Relationship(back_populates="subgroup", link_model=EventSubgroup)
    direction: Direction = Relationship(back_populates="subgroups")
