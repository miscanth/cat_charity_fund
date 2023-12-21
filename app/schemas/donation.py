from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationBase(BaseModel):
    """Базовый класс схемы"""
    full_amount: Optional[PositiveInt]
    comment: Optional[str] = Field(None, min_length=1)


class DonationCreate(DonationBase):
    """Схема для создания нового объекта пожертвования."""
    full_amount: PositiveInt


class DonationDB(DonationBase):
    """Схема ответа, возвращаемого из БД для метода Create."""
    full_amount: PositiveInt
    comment: Optional[str]
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationReadDB(DonationDB):
    """Схема ответа, возвращаемого из БД для метода Read."""
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
