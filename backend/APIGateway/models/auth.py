from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal, List, Union

class Group(BaseModel):
    name: str

class UniversalM(BaseModel):
    name: str
    type: Literal["Teacher","Location","Group"]
class MixedItems(BaseModel):
    items: List[Union[UniversalM, List[UniversalM]]]
    id: Optional[int] = None

class InternalUser(BaseModel):
    name: str
    theme: bool
    group: Group | None = None
    mostSearched: List[UniversalM] | None = None
    lastSearched: List[UniversalM] | None = None
    favorite: List[MixedItems]| None = None

class User(BaseModel):
    password: str

class SignupUser(User):
    email: EmailStr
class SigninUser(User):
    username: str

class ResponseToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class ResponseTokenInfo(ResponseToken):
    initial_info: InternalUser

class SessionId(BaseModel):
    session_id: int