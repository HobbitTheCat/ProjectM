from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Superman(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    username: str # теперь тоже может быть не уникальным
    hash: str # может быть не уникальным
    active: bool = Field(default=True)

    last_login: datetime|None
    try_number: int = Field(default=0)
    block: datetime|None

    sessions: list["Session"] = Relationship(back_populates="user")

class Session(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    time_stamp: datetime
    last_login: datetime
    ip: str|None = Field(default=None)
    device: str|None = Field(default=None)
    firebase_id: str|None = Field(default=None)

    is_active: bool = Field(default=True)

    refresh_token: str|None = Field(default=None)
    access_token: str|None = Field(default=None)

    user_id: int = Field(foreign_key="superman.id")
    user: Superman = Relationship(back_populates="sessions")