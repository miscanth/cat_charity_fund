from datetime import datetime

from sqlalchemy import Boolean, DateTime, Column, Integer

from app.core.config import settings
from app.core.db import Base


INVESTED_DEFAULT_VALUE = 0
TIME_FORMAT = (datetime.now()).isoformat(timespec='minutes')


class AbstractModel(Base):
    __abstract__ = True

    full_amount = Column(Integer(), nullable=False)
    invested_amount = Column(Integer(), default=settings.INVESTED_DEFAULT_VALUE)
    fully_invested = Column(Boolean(), default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, nullable=True)
