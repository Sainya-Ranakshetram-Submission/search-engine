"""
Enters BASE data
"""

import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from main.models import ToBeCrawledWebPages


class Command(BaseCommand):
    help = "Enters BASE data"
    requires_system_checks = output_transaction = True
        
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting Migration'))
        with open(settings.BASE_DIR / os.path.join("main", "management", "commands","data","dump_data_new.csv"),"r",newline='') as f:
            csvr=csv.reader(f,delimiter=',')
            sites_url_data = [rec[0] for rec in csvr]
        for i in sites_url_data:
            try:
                data_model=ToBeCrawledWebPages(url=i)
                data_model.save()
                self.stdout.write(self.style.SUCCESS(f'Migrated: {i}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Problem in migration of "{i}": {e}'))
        self.stdout.write(self.style.NOTICE(f'{len(sites_url_data)} url(s) migrated'))
        self.stdout.write('Now run `python manage.py crawl_to_be_crawled` command')
        