from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, Extra, root_validator, validator


TIME_FORMAT = (datetime.now()).isoformat(timespec='minutes')



class CharityProjectBase(BaseModel):
    """Базовый класс схемы"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid

    
class CharityProjectCreate(CharityProjectBase):
    """Схема для создания нового объекта проекта."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase): 
    pass

    @validator('name')
    def name_cant_be_null(cls, value: str):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым!')
        return value 
    
    """@root_validator(skip_on_failure=True)
    def fields_cannot_be_null(cls, values):
        for field in ['name', 'description']:
            if values[field] is None:
                raise ValueError('Данное поле проекта не может быть пустым!')
        return values"""
    
    


class CharityProjectDB(CharityProjectCreate):
    """Схема ответа, возвращаемого из БД."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True

