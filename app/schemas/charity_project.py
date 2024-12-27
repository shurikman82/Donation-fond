from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, Extra, Field, PositiveInt, root_validator, validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100, min_length=1)
    description: Optional[str] = Field(...)
    full_amount: Optional[PositiveInt]


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=100, min_length=1)
    description: str = Field(...)
    full_amount: PositiveInt


class CharityProjectDb(CharityProjectCreate):
    name: str
    description: str
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, max_length=100, min_length=1)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = Field(None)

    @validator('full_amount')
    def check_full_amount(cls, v):
        if not v:
            raise HTTPException(status_code=422, detail='Поле full_amount не может быть пустым')
        return v
    
    @validator('name')
    def check_name(cls, v):
        if not v:
            raise HTTPException(status_code=422, detail='Поле name не может быть пустым')
        return v
    
    @validator('description')
    def check_description(cls, v):
        if not v:
            raise HTTPException(status_code=422, detail='Поле description не может быть пустым')
        return v
    
    class Config:
        extra = Extra.forbid

class CharityProjectDbforSuperUser(CharityProjectDb):
    close_date: Optional[datetime]