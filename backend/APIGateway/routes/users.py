from fastapi import APIRouter, HTTPException
import requests
from starlette import status

from models.users import User

userRouter = APIRouter(
    tags=["users"]
)

AccessControlServiceURLSignup = ...
AccessControlServiceURLSignin = ...

@userRouter.post("/api/v1/auth/signup")
async def signupUser(user: User) -> dict:
    response = None
    try:
        response = requests.post(AccessControlServiceURLSignup, json=user.model_dump())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == status.HTTP_409_CONFLICT:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The email is already registered. Please use another email."
            )
        else:
            raise HTTPException(
                status_code = response.status_code,
                detail = response.json().get("detail", "An error occurred")
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AccessControlService is currently unavailable"
        )

@userRouter.post("/api/v1/auth/signin")
async def loginUser(user: User) -> dict:
    response = None
    try:
        response = requests.post(AccessControlServiceURLSignin, json=user.model_dump())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The user {user.username} was not found."
            )
        else:
            raise HTTPException(
                status_code = response.status_code,
                detail = response.json().get("detail", "An error occurred")
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AccessControlService is currently unavailable"
        )