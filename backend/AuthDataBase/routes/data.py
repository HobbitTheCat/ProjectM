from fastapi import APIRouter
from dataBase.dataBaseConection import DataBase
from models.data import Mail, MailResponse, User

dataRouter = APIRouter(
    tags=["data"]
)

@dataRouter.post("/api/v1/internal/data/check-mail", response_model=MailResponse)
async def check_mail(email: Mail) -> dict:
    with DataBase() as db:
        if db.existUser(email.email):
            return {
                "status": True,
                "hash": db.getHash(email.email),
            }
    return {"status": False}

@dataRouter.post("/api/v1/internal/data/create-user")
async def create_user(user: User) -> dict:
    with DataBase() as db:
        if db.insertUser(user.email, user.password):
            return {"status": "User created successfully"}
    return {"status": "User already exists"}

@dataRouter.post("/api/v1/internal/data/remove-user")
async def delete_user(user: User) -> dict:
    with DataBase() as db:
        if db.deleteUser(user.email):
            return {"status": "User successfully removed"}
    return {"status": "User removal failed, user not found"}