from datetime import datetime
from typing import Optional, Text

from pydantic import BaseModel, Field, PositiveInt, validator


class DonationBase(BaseModel):
    full_amount: PositiveInt = Field(...)
    comment: Optional[Text]


class DonationCreate(DonationBase):
    pass


class DonationUpdate(DonationBase):
    pass


class DonationDb(DonationBase):
    id: int
    create_date: datetime
    full_amount: PositiveInt

    class Config:
        orm_mode = True


class DonationDBforSuperUser(DonationDb):
    user_id: int
    invested_amount: int
    fully_invested: bool
