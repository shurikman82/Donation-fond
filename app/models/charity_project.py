from datetime import datetime as dt

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.db import Base


class CharityProject(Base):
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, nullable=False, default=dt.now)
    close_date = Column(DateTime)

    def __repr__(self):
        return f'Проект {self.name}, целевой сбор {self.full_amount}'
