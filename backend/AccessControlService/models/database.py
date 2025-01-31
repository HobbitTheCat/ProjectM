from sqlmodel import SQLModel, Field

class UserHash(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    hash: str = Field(unique=True)