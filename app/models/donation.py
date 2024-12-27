from datetime import datetime as dt

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.db import Base


class Donation(Base):
    comment = Column(Text, nullable=True)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, nullable=False, default=dt.now)
    close_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
