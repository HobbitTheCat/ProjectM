import httpx, os
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv

from models.user import User, TokenResponse, Mail
from auth.hash_password import HashPassword
from auth.jwt_handler import create_jwt_token

userRouter = APIRouter(
    tags=["userAccount"]
)

hashPassword = HashPassword()
load_dotenv()

DataBaseServiceURLCheckExistence = os.getenv("DATA_BASE_SERVICE_URL_CHECK_EXISTENCE")
DataBaseServiceURLAddUser = os.getenv("DATA_BASE_SERVICE_URL_ADD_USER")
DataBaseServiceURLRemoveUser = os.getenv("DATA_BASE_SERVICE_URL_REMOVE_USER")

@userRouter.post("/api/v1/internal/auth/signup")
async def signupUser(user: User) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            mailData = Mail(email=user.email)
            response = await client.post(
                url=DataBaseServiceURLCheckExistence,
                json = mailData.model_dump(),
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


@userRouter.post("/api/v1/internal/auth/signin", response_model=TokenResponse)
async def signinUser(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            mailData = Mail(email=user.username)
            response = await client.post(
                DataBaseServiceURLCheckExistence,
                json = mailData.model_dump(),
            )
            response.raise_for_status()
            if not response.json().get("status", False):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User with email does not exist")
            if hashPassword.verify_hash(user.password, response.json().get("hash")):
                access_token = create_jwt_token(user.username)
                return {
                    "access_token": access_token,
                    "token_type": "Bearer",
                }
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid details passed")
    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail=f"Failed to connect to email check service: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@userRouter.post("/api/v1/internal/auth/remove")
async def deleteUser(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            mailData = Mail(email=user.username)
            response = await client.post(
                url=DataBaseServiceURLCheckExistence,
                json = mailData.model_dump(),
            )
            response.raise_for_status()
            if not response.json().get("status", False):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User with email does not exist")
            if hashPassword.verify_hash(user.password, response.json().get("hash")):
                try:
                    async with httpx.AsyncClient() as client2:
                        delete_user = User(email=user.username, password=user.password)
                        response = await client2.post(
                            url=DataBaseServiceURLRemoveUser,
                            json = delete_user.model_dump(),
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