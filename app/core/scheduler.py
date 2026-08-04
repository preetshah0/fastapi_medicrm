import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.db.database import session
from app.services.appointment_service import mark_overdue_appointments

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


def _mark_overdue_job() -> None:
    db = session()
    try:
        count = mark_overdue_appointments(db)
        if count:
            logger.info(f"[Scheduler] Marked {count} appointment(s) as overdue.")
        else:
            logger.debug("[Scheduler] No overdue appointments found.")
    except Exception as e:
        logger.error(f"[Scheduler] Error in mark_overdue_job: {e}", exc_info=True)
    finally:
        db.close()


def register_jobs() -> None:
    scheduler.add_job(
        _mark_overdue_job,
        trigger=CronTrigger(hour=0, minute=0),  
        id="mark_overdue_appointments",
        replace_existing=True,
        misfire_grace_time=60 * 60,  
    )
    logger.info("[Scheduler] Jobs registered.")
