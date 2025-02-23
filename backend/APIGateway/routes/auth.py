import httpx, os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from models.auth import SignupUser, ResponseTokenInfo, SigninUser, SessionId
from auth.token_check import authenticate
from utils.errorHandler import handle_httpx_exceptions

load_dotenv()

userAuthRouter = APIRouter(
    tags=["usersAuth"]
)

AccessControlServiceURLSignup = os.getenv("ACCESS_CONTROL_SERVICE_URL_SIGNUP")
AccessControlServiceURLSignin = os.getenv("ACCESS_CONTROL_SERVICE_URL_SIGNIN")
AccessControlServiceURLRemove = os.getenv("ACCESS_CONTROL_SERVICE_URL_REMOVE")
AccessControlServiceURLRefresh = os.getenv("ACCESS_CONTROL_SERVICE_URL_REFRESH")
AccessControlServiceURLLogout = os.getenv("ACCESS_CONTROL_SERVICE_URL_LOGOUT")
AccessControlServiceURLLogoutSession = os.getenv("ACCESS_CONTROL_SERVICE_URL_LOGOUT_SESSION")
AccessControlServiceURLLogoutAll = os.getenv("ACCESS_CONTROL_SERVICE_URL_LOGOUT_ALL")
AccessControlServiceURLSessionList = os.getenv("ACCESS_CONTROL_SERVICE_URL_SESSION_LIST")

@userAuthRouter.post("/api/v1/user/auth/signup")
async def signupUser(user: SignupUser) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url = AccessControlServiceURLSignup, json=user.model_dump())
            response.raise_for_status()
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        handle_httpx_exceptions(e)

async def send_user_request(url: str, data: dict) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url = url, data = data)
            response.raise_for_status()
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        handle_httpx_exceptions(e)

@userAuthRouter.post("/api/v1/user/auth/signin", response_model=ResponseTokenInfo)
async def signinUser(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    return await send_user_request(AccessControlServiceURLSignin, SigninUser(username=user.username, password=user.password).model_dump())

@userAuthRouter.delete("/api/v1/user")
async def deleteUser(token: str = Depends(authenticate)) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url = AccessControlServiceURLRemove, headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        handle_httpx_exceptions(e)

@userAuthRouter.get("/api/v1/user/auth/refresh")
async def refreshToken(refresh_token: str = Depends(authenticate)) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=AccessControlServiceURLRefresh, headers={"Authorization": f"Bearer {refresh_token}"})
            response.raise_for_status()
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        handle_httpx_exceptions(e)

@userAuthRouter.post("/api/v1/user/auth/logout")
async def logoutUser(token: str = Depends(authenticate)) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url=AccessControlServiceURLLogout, headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        handle_httpx_exceptions(e)

@userAuthRouter.post("/api/v1/user/auth/logout-session")
async def logoutSession(userSession: SessionId, token: str = Depends(authenticate)) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url=AccessControlServiceURLLogoutSession, headers={"Authorization": f"Bearer {token}"}, json=userSession.model_dump())
            response.raise_for_status()
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        handle_httpx_exceptions(e)

@userAuthRouter.post("/api/v1/user/auth/logout-all")
async def logoutUser(token: str = Depends(authenticate)) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url=AccessControlServiceURLLogoutAll, headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        handle_httpx_exceptions(e)

@userAuthRouter.get("/api/v1/user/auth/session")
async def getSessionList(token: str = Depends(authenticate)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=AccessControlServiceURLSessionList, headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        handle_httpx_exceptions(e)