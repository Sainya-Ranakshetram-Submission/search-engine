"""
 Scraping newly entered sites in database
"""

import subprocess

from django.core.management.base import BaseCommand
from search_engine.celery import crawl, find_subdomains
from main.models import ToBeCrawledWebPages, CrawledWebPages


class Command(BaseCommand):
    help = "Scraps newly entered sites in database"
    requires_system_checks = output_transaction = True
    
    def add_arguments(self, parser):
        parser.add_argument(
            'amount',
            help='Amount of the domain(s) to be extracted from database',
            nargs='?',
            type=int
        )
        
    def handle(self, *args, **options):
        if options.get('amount'):
            amount=options.get('amount')
        
        for i in ToBeCrawledWebPages.objects.iterator():
            if not CrawledWebPages.objects.filter(url__in=i.url).exists():
                if i.scan_internal_links:
                    find_subdomains.delay(i.url)
                if not CrawledWebPages.objects.filter(url__in=i.url).exists():
                    self.stdout.write(self.style.NOTICE(f'Start Crawling {i}'))
                    crawl.delay(i.url)
                    self.stdout.write(self.style.SUCCESS("Done"))
    
    def give_start_urls(self,domain: str):
        a=subprocess.run(["subfinder", "-d", domain], capture_output=True)
        return list(map(lambda a: f'https://{a}',str(a.stdout.decode()).strip().split('\n')))
        