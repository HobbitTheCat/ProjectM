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

class SignupUser(BaseModel):
    email: EmailStr
    password: str

class AdditionalInfo(BaseModel):
    ip: Optional[str] = None
    device: Optional[str] = None
    firebase_id: Optional[str] = None

class ResponseToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class ResponseTokenInfo(ResponseToken):
    initial_info: InternalUser | None = None

class UserSession(BaseModel):
    currentSession: bool = False
    session_id: int
    creationTime: datetime
    lastLoginTime: datetime

class SessionId(BaseModel):
    session_id: int