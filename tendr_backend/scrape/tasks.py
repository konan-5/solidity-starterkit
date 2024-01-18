from config import celery_app
from tendr_backend.scrape.engine.tender import main
from tendr_backend.scrape.models import Tender

# User = get_user_model()


@celery_app.task()
def scrape_tender():
    """A pointless Celery task to demonstrate usage."""
    items = main(1)
    for data in items:
        try:
            tender = Tender(
                title=data["title"],
                resource_id=data["resource_id"],
                ca=data["ca"],
                info=data["info"],
                date_published=data["date_published"],
                tenders_submission_deadline=data["tenders_submission_deadline"],
                procedure=data["procedure"],
                status=data["status"],
                notice_pdf=data["notice_pdf"],
                award_date=data["award_date"],
                estimated_value=data["estimated_value"],
                cycle=data["cycle"],
            )
            tender.save()
        except Exception as e:
            print(e)
    return
