from sqlalchemy import Column, String

from .base import AbstractModel


class CharityProject(AbstractModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(100), nullable=False)
