from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "test@mail.com",
                "password": "password",
            }
        }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str