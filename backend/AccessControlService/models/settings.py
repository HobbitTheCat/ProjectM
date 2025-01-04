from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    SECRET_KEY: Optional[str]

    class Config:
        env_file = ".env"