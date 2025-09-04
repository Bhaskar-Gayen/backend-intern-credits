from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Credit
from app.utils import UserNotFound, InsufficientCredits
from datetime import datetime


class CreditService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_credit_balance(self, user_id: int):
        result = await self.db.execute(select(Credit).where(Credit.user_id == user_id))
        credit = result.scalar_one_or_none()
        if not credit:
            raise UserNotFound(user_id)
        return credit

    async def add_credits(self, user_id: int, amount: int):
        credit = await self.get_credit_balance(user_id)
        credit.credits += amount
        credit.last_updated = datetime.now()
        await self.db.commit()
        await self.db.refresh(credit)
        return credit

    async def deduct_credits(self, user_id: int, amount: int):
        credit = await self.get_credit_balance(user_id)
        if credit.credits < amount:
            raise InsufficientCredits(credit.credits, amount)

        credit.credits -= amount
        credit.last_updated = datetime.now()
        await self.db.commit()
        await self.db.refresh(credit)
        return credit

    async def reset_credits(self, user_id: int):
        credit = await self.get_credit_balance(user_id)
        credit.credits = 0
        credit.last_updated = datetime.now()
        await self.db.commit()
        await self.db.refresh(credit)
        return credit