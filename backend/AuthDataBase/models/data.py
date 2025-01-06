from pydantic import BaseModel, EmailStr
from typing import Optional

class Mail(BaseModel):
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "email": "test_user@mail.com",
            }
        }

class MailResponse(BaseModel):
    status: bool
    hash: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "hash": "<PASSWORD HASH>",
            }
        }

class User(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "test@gmail.com",
                "password": "<PASSWORD HASH>",
            }
        }