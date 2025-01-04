import httpx, os
from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from models.user import User, TokenResponse
from auth.hash_password import HashPassword
from auth.jwt_handler import create_jwt_token

userRouter = APIRouter(
    tags=["userAccount"]
)

hashPassword = HashPassword()

DataBaseServiceURLCheckExistence = os.getenv("DataBaseServiceURLCheckExistence")
DataBaseServiceURLAddUser = os.getenv("DataBaseServiceURLAddUser")

@userRouter.post("/api/v1/internal/auth/signup")
async def signupUser(user: User) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                DataBaseServiceURLCheckExistence,
                json = user.email
            )
        response.raise_for_status()
        answer = response.json().get("status", False)
        if answer:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email is already registered")
        hashedPassword = hashPassword.create_hash(user.password)
        user.password = hashedPassword
        try:
            async with httpx.AsyncClient() as client2:
                response = await client2.post(
                    DataBaseServiceURLAddUser,
                    json = user.model_dump()
                )
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                                detail=f"Failed to connect to downstream service: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail=f"Failed to connect to email check service: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@userRouter.post("/api/v1/internal/auth/signin")
async def signinUser(user: OAuth2PasswordRequestForm) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                DataBaseServiceURLCheckExistence,
                json = user.username
            )
            response.raise_for_status()
            if not response.json().get("status", False):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User with email does not exist.")
            if hashPassword.verify_hash(user.password, response.json().get("hash")):
                access_token = create_jwt_token(user.username)
                return {
                    "access_token": access_token,
                    "token_type": "Bearer",
                }
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid details passed.")
    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail=f"Failed to connect to email check service: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

