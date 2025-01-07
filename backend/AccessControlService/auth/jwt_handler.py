from jose import jwt
from dotenv import load_dotenv
import time, os

load_dotenv()

def create_jwt_token(user: str):
    payload = {
        "user": user,
        "expires": time.time() + 3600
    }
    token = jwt.encode(
        payload,
        os.getenv('SECRET_KEY'),
        algorithm="HS256"
    )
    return token