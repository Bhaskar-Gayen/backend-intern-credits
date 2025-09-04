from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class CreditAmount(BaseModel):
    amount: int = Field(gt=0, description="Amount must be positive")


class CreditResponse(BaseModel):
    user_id: int
    credits: int
    last_updated: datetime

    class Config:
        from_attributes = True


class CreditUpdate(BaseModel):
    credits: int
    last_updated: datetime
    model_config = ConfigDict(from_attributes=True)