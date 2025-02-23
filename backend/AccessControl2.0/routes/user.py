import asyncio
import os
from typing import List, Optional

import httpx
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from routes.internal import notify_user_service, get_user_info, delete_user_service
from auth.hash_password import HashPassword
from models.user import AdditionalInfo, SignupUser, ResponseToken, UserSession, SessionId, ResponseTokenInfo
from database.postgres import async_session
from database.redis import get_redis
from sqlalchemy.orm import selectinload
from sqlmodel import select
from models.hash_database import Superman, Session
from datetime import datetime, timedelta
from auth.jwt_creator import create_access_token, create_refresh_token, verify_jwt_token
from redis.asyncio import Redis
userRouter = APIRouter(
    tags=["user"]
)

expiration = timedelta(minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
hashPassword = HashPassword()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/internal/auth/signin")
try_limit = 5
@userRouter.post("/api/v1/internal/auth/signup")
async def signupUser(user: SignupUser) -> dict:
    try:
        async with async_session() as session:
            result = await session.execute(select(Superman).where(Superman.username == user.email).where(Superman.active == True))
            if result.scalars().first():
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email is already registered")
            superman = Superman(username=user.email, hash=hashPassword.create_hash(user.password))
            session.add(superman)
            await session.commit()
            asyncio.create_task(notify_user_service(str(user.email), superman.id))
        return {"status": "User created successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#
@userRouter.post("/api/v1/internal/auth/signin", response_model=ResponseTokenInfo  )
async def signinUser(user: OAuth2PasswordRequestForm = Depends(), additionalInfo: Optional[AdditionalInfo] = None):
    try:
        async with async_session() as session:
            result = await session.execute(select(Superman).where(Superman.username == user.username).where(Superman.active == True))
            result = result.scalars().first()
            if result is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with email does not exist")
            if result.block:
                if result.block > datetime.now():
                    raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                                        detail=f"Account is temporarily locked. Please try again later. TimeEnd:{result.block}")
                if result.block < datetime.now():
                    result.block = None
                    result.try_number = 4
                    await session.commit()
            if result.try_number >= try_limit:
                result.block = datetime.now() + timedelta(seconds=30)
                await session.commit()
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                                    detail=f"Account is temporarily locked. Please try again later. TimeEnd:{result.block}")
            if not hashPassword.verify_hash(user.password, result.hash):
                result.try_number += 1
                await session.commit()
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid details passed")

            result.try_number = 0
            currentTime = datetime.now()
            result.last_login = currentTime
            newSession = Session(time_stamp=currentTime, last_login=currentTime, user=result,
                                 ip=additionalInfo.ip if additionalInfo else None,
                                 device= additionalInfo.device if additionalInfo else None,
                                 firebase_id = additionalInfo.firebase_id if additionalInfo else None)
            session.add(newSession)
            await session.commit() # добавить try except блок
            await session.refresh(newSession)
            refreshToken = create_refresh_token(newSession.id, result.id)
            access_token = create_access_token(newSession.id, result.id)
            newSession.refresh_token = refreshToken
            newSession.access_token = access_token
            await session.commit()
            user_info = None
        try:
            user_info = await get_user_info(access_token)
        except httpx.ConnectError: print("Connection error")
        return ResponseTokenInfo(access_token=access_token, refresh_token=refreshToken, token_type="Bearer", initial_info=user_info if user_info else None)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@userRouter.delete("/api/v1/internal/auth/user")
async def deleteUser(accessToken:str = Depends(oauth2_scheme), redis: Redis = Depends(get_redis)):
    try:
        payload = verify_jwt_token(accessToken)
        async with async_session() as session:
            user_id = payload["user_id"]
            query = select(Superman).where(Superman.id == user_id).where(Superman.active == True)
            query = query.options(selectinload(Superman.sessions))
            result = await session.execute(query)
            result = result.scalars().first()
            if result is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            result.active = False
            await redis.set(accessToken, "expired", ex=int(expiration.total_seconds()))
            for item in result.sessions:
                item.is_active = False
                await redis.set(item.access_token, "expired",ex=int(expiration.total_seconds()))
            await session.commit()
            asyncio.create_task(delete_user_service(accessToken))
        return {"status": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ,response_model=ResponseToken
@userRouter.get("/api/v1/internal/auth/refresh")
async def refreshUser(refreshToken: str = Depends(oauth2_scheme)):
    try:
        payload = verify_jwt_token(refreshToken, True)
        async with async_session() as session:
            query = select(Session).where(Session.id ==  payload["session_id"]).where(Session.is_active == True)
            query = query.options(selectinload(Session.user))
            result = await session.execute(query)
            result = result.scalars().first()
            if result is None or result.refresh_token != refreshToken:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session does not exist") # если выпадает эта ошибка срочно выйти из сессии
            currentTime = datetime.now()
            result.last_login = currentTime
            refreshToken = create_refresh_token(result.id, result.user.id)
            access_token = create_access_token(result.id, result.user.id)
            result.refresh_token = refreshToken
            result.access_token = access_token
            await session.commit()
        return ResponseToken(access_token=access_token, refresh_token=refreshToken,  token_type="Bearer")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@userRouter.post("/api/v1/internal/auth/logout")
async def logoutUser(accessToken:str = Depends(oauth2_scheme), redis: Redis = Depends(get_redis)) -> dict:
    try:
        payload = verify_jwt_token(accessToken)
        async with async_session() as session:
            sessionId = payload["session_id"]
            result = await session.execute(select(Session).where(Session.id == sessionId).where(Session.is_active == True))
            result = result.scalars().first()
            result.is_active = False
            await redis.set(accessToken, "expired", ex=int(expiration.total_seconds()))
            await session.commit()
        return {"status": "User logged out successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@userRouter.post("/api/v1/internal/auth/logout-session")
async def logoutSession(userSession: SessionId, accessToken:str = Depends(oauth2_scheme), redis: Redis = Depends(get_redis)):
    try:
        payload = verify_jwt_token(accessToken)
        async with async_session() as session:
            query = select(Session).where(Session.id == userSession.session_id).where(Session.is_active == True)
            query.options(selectinload(Session.user))
            result = await session.execute(query)
            result = result.scalars().first()
            if result is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session does not exist")
            if result.user_id != payload["user_id"]:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not the right user")
            result.is_active = False
            await redis.set(result.access_token, "expired", ex=int(expiration.total_seconds()))
            await session.commit()
        return {"status": "User logged out successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@userRouter.post("/api/v1/internal/auth/logout-all")
async def logoutAllSession(accessToken:str = Depends(oauth2_scheme), redis: Redis = Depends(get_redis)):
    try:
        payload = verify_jwt_token(accessToken)
        async with async_session() as session:
            userId = payload["user_id"]
            results = await session.execute(select(Session).where(Session.user_id == userId).where(Session.is_active == True))
            results = results.scalars().all()
            countOfRemovedSessions = 0
            for result in results:
                if result.id != payload["session_id"]:
                    result.is_active = False
                    countOfRemovedSessions += 1
                    await redis.set(result.access_token, "expired", ex=int(expiration.total_seconds()))
            await session.commit()
        return {"status": "Session logged out successfully", "countOfRemovedSessions": countOfRemovedSessions}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@userRouter.get("/api/v1/internal/auth/session", response_model=List[UserSession])
async def getSessions(accessToken:str = Depends(oauth2_scheme)):
    try:
        payload = verify_jwt_token(accessToken)
        async with async_session() as session:
            userId = payload["user_id"]
            results = await session.execute(select(Session).where(Session.user_id == userId).where(Session.is_active == True))
            results = results.scalars().all()
            response = []
            for result in results:
                session = UserSession(creationTime=result.time_stamp, lastLoginTime=result.last_login, session_id=result.id)
                if result.id == payload["session_id"]:
                    session.currentSession = True
                response.append(session)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
