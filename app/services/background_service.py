from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.core.database import AsyncSessionLocal
from app.models import Credit
from datetime import datetime
import logging


class BackgroundService:

    @staticmethod
    async def add_daily_credits():
        async with AsyncSessionLocal() as db:
            try:
                await db.execute(
                    update(Credit)
                    .values(credits=Credit.credits + 5, last_updated=datetime.utcnow())
                )
                await db.commit()

                result = await db.execute(select(Credit))
                count = len(result.scalars().all())
                logging.info(f"Added 5 credits to {count} users")

            except Exception as e:
                await db.rollback()
                logging.error(f"Failed to add daily credits: {e}")

    @staticmethod
    def start_daily_task():
        from app.core.scheduler import add_daily_job
        add_daily_job(BackgroundService.add_daily_credits)