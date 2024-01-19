from django.core.management.base import BaseCommand

from tendr_backend.scrape.models import CftFile, ClientInfo, Tender


class Command(BaseCommand):
    help = "My shiny new management command."

    # def add_arguments(self, parser):
    #     parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        Tender.objects.all().delete()
        CftFile.objects.all().delete()
        ClientInfo.objects.all().delete()
