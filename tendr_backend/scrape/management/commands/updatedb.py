from django.core.management.base import BaseCommand

from tendr_backend.scrape.models import Tender


class Command(BaseCommand):
    help = "My shiny new management command."

    # def add_arguments(self, parser):
    #     parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        tenders = Tender.objects.all()
        for tender in tenders:
            if tender.cpv_code is None:
                print(tender.pk, tender.resource_id)
