from fastapi import APIRouter
from dataBase.dataBaseConection import DataBase
from models.data import *

dataRouter = APIRouter(
    tags=["data"]
)

dataBase = DataBase()

@dataRouter.get("/api/v1/internal/data/check-mail", response_model=MailResponse)
async def check_mail(email: Mail) -> dict:
    if dataBase.existUser(email):
        return {
            "status": True,
            "hash": dataBase.getHash(email),
            }
    return {"status": False}

@dataRouter.post("/api/v1/internal/data/user")
async def create_user(user: User) -> dict:
    if dataBase.insertUser(user.email, user.password):
        return {"message": "User created successfully"}
    return {"message": "User creation failed"}
