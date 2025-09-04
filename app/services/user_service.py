from fastapi import FastAPI
from pydantic import EmailStr
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User, Credit
from app.schemas import UserCreate
from app.utils import UserNotFound, EmailIdAlreadyExist


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_user_exist(self, email: EmailStr):
        try:
            result=await self.db.execute(select(User).where(User.email==email))
            user = result.scalar_one_or_none()
            if user:
                raise EmailIdAlreadyExist(email)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to find user from DB:  {str(e)}")

    async def get_user(self, user_id: int):
        try:
            result = await self.db.execute(select(User).where(User.user_id == user_id))
            user = result.scalar_one_or_none()
            if not user:
                raise UserNotFound(user_id)
            return user
        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to create user: {str(e)}")

    async def create_user(self, user_data: UserCreate):
        try:
            await  self.check_user_exist(user_data.email)
            user = User(**user_data.model_dump())
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)

            credit = Credit(user_id=user.user_id, credits=0)
            self.db.add(credit)
            await self.db.commit()

            return user

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError(f"Failed to create user: {str(e)}")

    async def get_all_users(self):
        result = await self.db.execute(select(User))
        return result.scalars().all()


