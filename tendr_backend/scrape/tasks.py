from config import celery_app

# User = get_user_model()


@celery_app.task()
def scrape_tender():
    """A pointless Celery task to demonstrate usage."""
    # users = User.objects.count()
    print("start - scrape tender")
    return
