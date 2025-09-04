from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.start()
    logging.info("Scheduler started")

def stop_scheduler():
    scheduler.shutdown()
    logging.info("Scheduler stopped")

def add_daily_job(func, hour=0, minute=0):
    scheduler.add_job(
        func,
        CronTrigger(hour=hour, minute=minute, timezone='UTC'),
        id='daily_credit_update'
    )