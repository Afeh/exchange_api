from decouple import config
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = config("DATABASE_URL")

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()