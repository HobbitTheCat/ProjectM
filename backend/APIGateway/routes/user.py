import httpx, os
from dotenv import load_dotenv
from fastapi import APIRouter,Depends

from models.schedule import MixedItems, UniversalM
from auth.token_check import authenticate
from utils.errorHandler import handle_httpx_exceptions
from models.user import UpdateThemeRequest, UpdateBirthdayRequest, UpdateNameRequest, Group

load_dotenv()
userRouter = APIRouter(
    tags=["users"]
)
GetUserUrl = os.getenv("GET_USER_URL")
HistoryUserUrl = os.getenv("HISTORY_USER_URL")
FavoriteUserUrl = os.getenv("FAVORITE_USER_URL")
ChangeNameUrl = os.getenv("CHANGE_NAME_URL")
ChangeBirthdayUrl = os.getenv("CHANGE_BIRTHDAY_URL")
ChangeGroupUrl = os.getenv("CHANGE_GROUP_URL")
ChangeThemeUrl = os.getenv("CHANGE_THEME_URL")

async def send_put_request(url: str, data: dict, token: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                url,
                json=data,
                headers = {"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        handle_httpx_exceptions(e)

async def send_post_request(url: str, data, token: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=data,
                headers = {"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        handle_httpx_exceptions(e)

@userRouter.put("/api/v1/user/name")
async def changeUserName(request: UpdateNameRequest, token: str = Depends(authenticate)) -> dict:
    return await send_put_request(url=ChangeNameUrl, data=request.model_dump(), token=token)

@userRouter.put("/api/v1/user/birthday")
async def changeUserBirthday(request: UpdateBirthdayRequest, token: str = Depends(authenticate)) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(url=ChangeBirthdayUrl, json={"birthday": str(request.birthday)}, headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as e: handle_httpx_exceptions(e)

@userRouter.put("/api/v1/user/group")
async def changeUserGroup(request: Group, token: str = Depends(authenticate)) -> dict:
    return await send_put_request(url=ChangeGroupUrl, data=request.model_dump(), token=token)

@userRouter.put("/api/v1/user/theme")
async def changeUserTheme(request: UpdateThemeRequest, token: str = Depends(authenticate)) -> dict:
    return await send_put_request(url=ChangeThemeUrl, data=request.model_dump(), token=token)

@userRouter.post("/api/v1/user/favorite")
async def addGroupFavorite(group: MixedItems, token: str = Depends(authenticate)):
    return await send_post_request(FavoriteUserUrl, group.model_dump(), token)

@userRouter.post("/api/v1/user/history")
async def addLastSearched(last_searched: UniversalM, token: str = Depends(authenticate)):
    return await send_post_request(HistoryUserUrl, last_searched.model_dump(), token)

@userRouter.delete("/api/v1/user/favorite")
async def deleteFavorite(index: int, token: str = Depends(authenticate)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url=f"{FavoriteUserUrl}?index={index}", headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        handle_httpx_exceptions(e)

@userRouter.get("/api/v1/user")
async def getUser(token: str = Depends(authenticate)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=GetUserUrl, headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        handle_httpx_exceptions(e)
