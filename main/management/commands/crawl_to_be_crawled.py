"""
 Scraping newly entered sites in database
"""

import subprocess

from django.core.management.base import BaseCommand
from main.models import ToBeCrawledWebPages


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
            if i.scan_internal_links:
                self.stdout.write(self.style.NOTICE('Finding Sudomains of', i.url))
                subdomains = self.give_start_urls(i.url)
                self.stdout.write(self.style.NOTICE('Submitting the subdomains to database'))
                self.stdout.write(self.style.SUCCESS(subdomains))
                self.stdout.write(self.style.NOTICE('Starting Migration of Subdoamins'))
                for j in subdomains:
                    try:
                        a=ToBeCrawledWebPages(url=j,scan_internal_links=False)
                        a.save()
                        self.stdout.write(self.style.SUCCESS(f'Migrated: {j}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Problem in migration of "{j}": {e}'))
                self.stdout.write(self.style.SUCCESS('Done'))
            self.stdout.write(self.style.NOTICE('Start Crawling', i))
            subprocess.run(["scrapy", "crawl", "konohagakure_to_be_crawled", "-a", f"allowed_domains={i.url}"], capture_output=False)
            self.stdout.write(self.style.SUCCESS("Done"))
    
    def give_start_urls(self,domain: str):
        a=subprocess.run(["subfinder", "-d", domain], capture_output=True)
        return list(map(lambda a: f'https://{a}',str(a.stdout.decode()).strip().split('\n')))
        