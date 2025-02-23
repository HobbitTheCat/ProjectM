from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from database.redis import get_redis
from redis.asyncio import Redis

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin")

async def authenticate(token: str = Depends(oauth2_scheme), redis: Redis = Depends(get_redis)) -> str:
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Sign in for access")
    state = await redis.get(token)
    if not state is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired")
    return token
