from pydantic import BaseModel
from datetime import date
from typing import Literal

class UpdateNameRequest(BaseModel):
    name: str

class UpdateBirthdayRequest(BaseModel):
    birthday: date

class UpdateThemeRequest(BaseModel):
    theme: Literal["light", "dark"]

