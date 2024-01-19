import time

from django.core.management.base import BaseCommand

from tendr_backend.scrape.engine.tender import main


class Command(BaseCommand):
    help = "My shiny new management command."

    # def add_arguments(self, parser):
    #     parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        for i in range(1, 42):
            main(i)
            time.sleep(1)
