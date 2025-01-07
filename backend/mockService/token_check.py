import time, os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError


load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/signin")
secret_key = os.getenv('SECRET_KEY')

def verify_access_token(token: str):
    try:
        data = jwt.decode(token, secret_key, algorithms=['HS256'])
        expire = data.get('expires')

        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token provided"
            )
        currentTime = datetime.now(timezone.utc)
        expireTime = datetime.fromtimestamp(expire, timezone.utc)
        if currentTime > expireTime:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token expired"
            )
        return data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid access token"
        )

def authenticate(token: str = Depends(oauth2_scheme)) -> str:
    decoded = verify_access_token(token)
    return decoded["user"]