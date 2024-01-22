from celery import shared_task

from config import celery_app
from tendr_backend.scrape.engine.tender import main

# User = get_user_model()


@shared_task(time_limit=6000)
@celery_app.task()
def scrape_tender():
    """A pointless Celery task to demonstrate usage."""
    print("Start scrape task")
    main(1)
    print("End scrape task")
