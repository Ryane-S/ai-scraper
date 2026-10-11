import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.config import settings
from app.core.database import SessionLocal
from app.services.scraper import fetch_and_store_articles
from app.crud.article import delete_old_articles

# On instancie un logger
logger = logging.getLogger(__name__)

# On instancie le scheduler
scheduler = BackgroundScheduler(timezone="Europe/Paris")

def _run_scraping() -> None:
    logger.info("Job scraping démarré.")
    try:
        fetch_and_store_articles()
    except Exception as e:
        logger.exception("Erreur lors du scraping.")
    finally:
        logger.info("Scraping terminé !")

def _run_cleanup() -> None:
    logger.info("Job nettoyage démarré.")
    db = SessionLocal()
    try:
        # Date seuil
        threshold = datetime.now() - timedelta(days=settings.CLEANUP_DAYS_OLD)
        # Suppression
        deleted_articles = delete_old_articles(db, date=threshold)
        logger.info(f"Nombre d'articles supprimés: {deleted_articles}")
    except Exception as e:
        logger.exception("Erreur lors du nettoyage.")
    finally:
        db.close()
        logger.info("Job nettoyage terminé !")

def start_scheduler() -> None:
    if settings.DISABLE_SCHEDULER:
        logger.info("Scheduler désactivé.")
        return
    else:
        scheduler.add_job(
            func=_run_scraping, 
            trigger=CronTrigger(hour=settings.SCRAPE_HOUR, minute=0), 
            id="scraping",
            max_instances=1
        )
        scheduler.add_job(
            func=_run_cleanup,
            trigger=CronTrigger(hour=settings.CLEANUP_HOUR, minute=0),
            id="cleanup",
            max_instances=1
        )
        scheduler.start()
        for job in scheduler.get_jobs():
            logger.info(f"  → Job '{job.id}' prochaine exécution : {job.next_run_time}")
        logger.info("Scheduler démarré.")

def shutdown_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler arrêté.")