"""
 Scraping newly entered sites in database
"""

from django.conf import settings
import subprocess
from django.core.management import call_command
from django.core.management.base import BaseCommand
from main.models import ToBeCrawledWebPages
import scrapy


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
                print('Finding Sudomains of', i.url)
                subdomains = self.give_start_urls(i.url)
                print('Submitting the subdomains to database')
                print(subdomains)
                for j in subdomains:
                    try:
                        a=ToBeCrawledWebPages(url=j,scan_internal_links=False)
                        a.save()
                    except:
                        pass
                print('Done')
            print('Start Crawling', i)
            subprocess.run(["scrapy", "crawl", "konohagakure_to_be_crawled", "-a", f"allowed_domains={i.url}"], capture_output=False)
            print("Done")
    
    def give_start_urls(self,domain: str):
        a=subprocess.run(["subfinder", "-d", domain], capture_output=True)
        return list(map(lambda a: f'https://{a}',str(a.stdout.decode()).strip().split('\n')))
        