import os
from fastapi import HTTPException, status
from dotenv import load_dotenv
from authlib.jose import jwt

load_dotenv()
secretKey = os.getenv('SECRET_KEY')

def verify_jwt_token(token:str):
    try:
        if isinstance(token, str):
            token = token.encode("utf-8")
        payload = jwt.decode(token, secretKey)
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )