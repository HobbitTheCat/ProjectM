from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from models.database import UserHash
from database import async_session
from models.user import User, TokenResponse
from auth.hash_password import HashPassword
from auth.jwt_handler import create_jwt_token

userRouter = APIRouter(
    tags=["userAccount"]
)

hashPassword = HashPassword()

@userRouter.post("/api/v1/internal/auth/signup")
async def signupUser(user: User) -> dict:
    try:
        async with async_session() as session:
            query = select(UserHash).where(UserHash.name == user.email)
            result = await session.execute(query)
            result = result.scalars().first()
            if result is not None:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email is already registered")
            userHash = UserHash(name = user.email, hash = hashPassword.create_hash(user.password))
            session.add(userHash)
            await session.commit()
        return {"status": "User created successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@userRouter.post("/api/v1/internal/auth/signin", response_model=TokenResponse)
async def signinUser(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    try:
        async with async_session() as session:
            query = select(UserHash).where(UserHash.name == user.username)
            result = await session.execute(query)
            result = result.scalars().first()
            if result is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with email does not exist")
            if hashPassword.verify_hash(user.password, result.hash):
                access_token = create_jwt_token(user.username)
                return {
                    "access_token": access_token,
                    "token_type": "Bearer",
                }
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid details passed")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@userRouter.post("/api/v1/internal/auth/remove")
async def deleteUser(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    try:
        async with async_session() as session:
            query = select(UserHash).where(UserHash.name == user.username)
            result = await session.execute(query)
            result = result.scalars().first()
            if result is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with email does not exist")
            if hashPassword.verify_hash(user.password, result.hash):
                await session.delete(result)
                await session.commit()
                return {"status": "User successfully removed"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))