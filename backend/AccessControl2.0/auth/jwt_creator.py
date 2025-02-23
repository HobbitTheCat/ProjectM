import os
from authlib.jose import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi import HTTPException, status
load_dotenv()

secretKey = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')
accessTokenExp = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
refreshTokenExp = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS'))

def create_access_token(session_id:int, user_id:int):
    to_encode = {"session_id": session_id, "user_id": user_id, "refresh": False}
    expire = datetime.now() + timedelta(minutes=accessTokenExp)
    to_encode.update({"exp": expire})
    return jwt.encode({"alg": algorithm}, to_encode, key=secretKey).decode("utf-8")

def create_refresh_token(session_id:int, user_id:int):
    to_encode = {"session_id": session_id, "user_id": user_id, "refresh": True}
    expire = datetime.now() + timedelta(days=refreshTokenExp)
    to_encode.update({"exp": expire})
    return jwt.encode({"alg": algorithm}, to_encode, key=secretKey).decode("utf-8")

def verify_jwt_token(token: str, isRefreshToken: bool = False):
    try:
        if isinstance(token, str):
            token = token.encode("utf-8")
        payload = jwt.decode(token, secretKey)
        if isRefreshToken:
            if not payload["refresh"]:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
            return payload
        if payload["refresh"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
        return payload
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token token")

# secretKeyCurrent = ""
# secretKeyOld = ""
# secretKeyExpire = ""
#
# def verify_jwt_token2(token: str, isRefreshToken: bool = False):
#     try:
#         if isinstance(token, str):
#             token = token.encode("utf-8")
#         keyExpire = datetime.strptime(secretKeyExpire, "%Y-%m-%d %H:%M:%S")
#         if keyExpire < datetime.now():
#             try:
#                 payload = jwt.decode(token, secretKeyOld)
#             except Exception:
#                 payload = jwt.decode(token, secretKeyCurrent)
#         else:
#             payload = jwt.decode(token, secretKeyCurrent)
#         if isRefreshToken:
#             if not payload["refresh"]:
#                 raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
#             return payload
#         if payload["refresh"]:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
#         return payload
#     except HTTPException as e:
#         raise e
#     except Exception:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

