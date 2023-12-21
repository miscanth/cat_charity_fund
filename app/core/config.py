from pydantic import BaseSettings

# from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Кошачий благотворительный фонд'
    app_description: str = 'Приложение для Благотворительного фонда поддержки котиков QRKot'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    INVESTED_DEFAULT_VALUE = 0
    # first_superuser_email: Optional[EmailStr] = None
    #  first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()