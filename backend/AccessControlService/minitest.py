from models.user import User
import asyncio
from routes.user import *
from pydantic import BaseModel

class UserWithUsername(BaseModel):
    username: str
    password: str

user = {"username": "egor@mail.com", "password": "<PASSWORD>"}
user = UserWithUsername.model_validate(user)
print(asyncio.run(deleteUser(user)))
