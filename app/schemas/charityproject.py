from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.core.config import settings


class CharityProjectBase(BaseModel):
    """Базовый класс схемы"""
    name: Optional[str] = Field(None, min_length=settings.MIN_LEN_FIELD, max_length=settings.MAX_LEN_FIELD)
    description: Optional[str] = Field(None, min_length=settings.MIN_LEN_FIELD)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания нового объекта проекта."""
    name: str = Field(..., min_length=settings.MIN_LEN_FIELD, max_length=settings.MAX_LEN_FIELD)
    description: str = Field(..., min_length=settings.MIN_LEN_FIELD)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass

    @validator('name')
    def name_cant_be_null(cls, value: str):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectCreate):
    """Схема ответа, возвращаемого из БД."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime = Field(default=None)

    class Config:
        orm_mode = True
