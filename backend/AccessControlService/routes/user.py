from fastapi import APIRouter, HTTPException
from models.user import User, TokenResponse

userRouter = APIRouter(
    tags=["users"]
)

@userRouter.post("/api/v1/internal/auth/signup")
async def signupUser(user: User) -> dict:
    userExist = ...