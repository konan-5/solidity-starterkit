from config import celery_app
from tendr_backend.scrape.engine.tender import main

# User = get_user_model()


@celery_app.task()
def scrape_tender():
    """A pointless Celery task to demonstrate usage."""
    main(1)
