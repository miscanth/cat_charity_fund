from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Кошачий благотворительный фонд'
    app_description: str = 'Приложение для Благотворительного фонда поддержки котиков QRKot'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    MIN_LEN_FIELD = 1
    MAX_LEN_FIELD = 100
    INVESTED_DEFAULT_VALUE = 0
    LIFETIME_SECONDS = 3600
    MIN_LEN_PASSWORD = 3
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
