from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True