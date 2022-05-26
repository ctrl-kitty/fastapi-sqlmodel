import os
from typing import Union, Optional, Any

from pydantic import BaseSettings, EmailStr

# todo ip validation
# todo разобраться с загрузкой .env переменных до создания ссылок к бд(не через проперти)


class Settings(BaseSettings):

    PROJECT_NAME: str = "FastAPI"
    DEBUG: bool = True
    BACKEND_PORT: Union[int, str] = 80
    BACKEND_HOST: str = "localhost"
    FIRST_SUPERUSER_EMAIL: EmailStr = "mail@gmail.com"
    FIRST_SUPERUSER_PASSWORD: str = "password"
    ACCESS_TOKEN_EXPIRE_MINUTES: Union[int, str] = 5 * 24 * 60
    ENCRYPT_KEY: str = "12345"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "password"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: Union[int, str] = 5432
    DATABASE_NAME: str = "db"

    def get_db_uri(self, adapter: str):
        return f"postgresql+{adapter}://{self.DATABASE_USER}:" \
               f"{self.DATABASE_PASSWORD}@" \
               f"{self.DATABASE_HOST}:" \
               f"{self.DATABASE_PORT}/" \
               f"{self.DATABASE_NAME}"

    def get_async_db_uri(self):
        return self.get_db_uri("asyncpg")

    def get_sync_db_uri(self):
        return self.get_db_uri("psycopg2")

    ASYNC_DATABASE_URI: Optional[
        Any
    ] = property(get_async_db_uri)
    SYNC_DATABASE_URI: Optional[
        Any
    ] = property(get_sync_db_uri)


    class Config:

        case_sensitive = True
        env_file = os.path.expanduser("~/.env")


settings = Settings()
