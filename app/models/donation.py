from sqlalchemy import Column, ForeignKey, Integer, String

from .base import AbstractModel


class Donation(AbstractModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(String(), nullable=True)
