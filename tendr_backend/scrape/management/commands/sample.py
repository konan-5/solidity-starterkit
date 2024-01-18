import time

from django.core.management.base import BaseCommand

from tendr_backend.scrape.engine.tender import main
from tendr_backend.scrape.models import Tender


class Command(BaseCommand):
    help = "My shiny new management command."

    # def add_arguments(self, parser):
    #     parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        # pass
        # all_tenders = Tender.objects.all()
        # resource_ids = [tender.resource_id for tender in all_tenders]
        # for resource_id in resource_ids:
        #     request_url = f"https://www.etenders.gov.ie/epps/cft/prepareViewCfTWS.do?resourceId={resource_id}"
        for i in range(41):
            items = main(i + 1)
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
            time.sleep(2)
