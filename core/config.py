import os
from typing import Union, Optional, Any
from pydantic import BaseSettings, EmailStr, IPvAnyAddress


class Settings(BaseSettings):
    PROJECT_NAME: str
    DEBUG: bool
    WORKERS_PER_THREAD: int
    BACKEND_PORT: Union[int, str]
    BACKEND_HOST: IPvAnyAddress
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    ACCESS_TOKEN_EXPIRE_MINUTES: Union[int, str]
    ENCRYPT_KEY: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: IPvAnyAddress
    DATABASE_PORT: Union[int, str]
    DATABASE_NAME: str

    def get_db_uri(self, adapter: str) -> str:
        return f"postgresql+{adapter}://{self.DATABASE_USER}:" \
               f"{self.DATABASE_PASSWORD}@" \
               f"{self.DATABASE_HOST}:" \
               f"{self.DATABASE_PORT}/" \
               f"{self.DATABASE_NAME}"

    def get_async_db_uri(self):
        return self.get_db_uri("asyncpg")

    def get_sync_db_uri(self):
        return self.get_db_uri("psycopg2")

    ASYNC_DATABASE_URI: Optional[Any] = property(get_async_db_uri)
    SYNC_DATABASE_URI: Optional[Any] = property(get_sync_db_uri)

    class Config:
        case_sensitive = True
        env_file = os.path.expanduser("~/.env")


settings = Settings()
