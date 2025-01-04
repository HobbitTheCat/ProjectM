from jose import jwt
from models.settings import Settings
import time

def create_jwt_token(user: str):
    payload = {
        "user": user,
        "expires": time.time() + 3600
    }
    token = jwt.encode(
        payload,
        Settings.SECRET_KEY,
        algorithm="HS256"
    )
    return token