import httpx, os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Union, List

from models.schedule import MixedItems
from models.users import User, TokenResponse, LoginPayload
from auth.token_check import authenticate

load_dotenv()

userAuthRouter = APIRouter(
    tags=["usersAuth"]
)
userRouter = APIRouter(
    tags=["users"]
)

AccessControlServiceURLSignup = os.getenv("ACCESS_CONTROL_SERVICE_URL_SIGNUP")
AccessControlServiceURLSignin = os.getenv("ACCESS_CONTROL_SERVICE_URL_SIGNIN")
AccessControlServiceURLRemove = os.getenv("ACCESS_CONTROL_SERVICE_URL_REMOVE")

AddFavoriteGroupURL = os.getenv("ADD_FAVORITE_GROUP_URL")
AddLastSearchedURL = os.getenv("ADD_LAST_SEARCHED_URL")
GetFavoriteGroupURL = os.getenv("GET_FAVORITE_GROUP_URL")
GetLastSearchedURL = os.getenv("GET_LAST_SEARCHED_URL")

@userAuthRouter.post("/api/v1/user/auth/signup")
async def signupUser(user: User) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url = AccessControlServiceURLSignup,
                json=user.model_dump()
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                                detail=f"Failed to connect to downstream service: {e}")
    except httpx.HTTPStatusError as e:
        try:
            errorDetail = e.response.json().get("detail", e.response.text)
        except ValueError:
            errorDetail = e.response.text
        raise HTTPException(status_code=e.response.status_code, detail=errorDetail)


async def send_user_request(url: str, data: dict) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url = url,
                data = data,
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                                detail=f"Failed to connect to downstream service: {e}")
    except httpx.HTTPStatusError as e:
        try:
            errorDetail = e.response.json().get("detail", e.response.text)
        except ValueError:
            errorDetail = e.response.text
        raise HTTPException(status_code=e.response.status_code, detail=errorDetail)

@userAuthRouter.post("/api/v1/user/auth/signin", response_model=TokenResponse)
async def signinUser(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    return await send_user_request(AccessControlServiceURLSignin, LoginPayload(username=user.username, password=user.password).model_dump())

@userAuthRouter.post("/api/v1/user/auth/remove")
async def removeUser(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    return await send_user_request(AccessControlServiceURLRemove, LoginPayload(username=user.username, password=user.password).model_dump())


async def send_post_request(url: str, data: dict, token: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=data,
                headers = {"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,detail=f"Failed to connect to downstream service: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@userRouter.post("/api/v1/user/favorite")
async def addGroupFavorite(group: MixedItems, token: str = Depends(authenticate)) -> dict:
    return await send_post_request(AddFavoriteGroupURL, group.model_dump(), token)

@userRouter.post("/api/v1/user/last-searched")
async def addLastSearched(last_searched: MixedItems, token: str = Depends(authenticate)):
    return await send_post_request(AddLastSearchedURL, last_searched.model_dump(), token)

async def send_get_request(url: str, token: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,detail=f"Failed to connect to downstream service: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@userRouter.get("/api/v1/user/favorite", response_model=MixedItems)
async def favorite(token: str = Depends(authenticate)):
    return await send_get_request(GetFavoriteGroupURL, token)

@userRouter.get("/api/v1/user/last-searched", response_model=MixedItems)
async def lastSearched(token: str = Depends(authenticate)):
    return await send_get_request(GetLastSearchedURL, token)
