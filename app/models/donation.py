from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from .base import AbstractModel


class Donation(AbstractModel):
    # user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(String())
