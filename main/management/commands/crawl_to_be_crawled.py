"""
 Scraping newly entered sites in database
"""

import subprocess

from django.core.management.base import BaseCommand
from main.models import ToBeCrawledWebPages, CrawledWebPages


class Command(BaseCommand):
    help = "Scraps newly entered sites in database"
    requires_system_checks = output_transaction = True
        
    def handle(self, *args, **options):
        for i in ToBeCrawledWebPages.objects.iterator():
            if not CrawledWebPages.objects.filter(url__in=i.url).exists():
                if i.scan_internal_links:
                    self.find_subdomains(i.url)
                if not CrawledWebPages.objects.filter(url__in=i.url).exists():
                    self.stdout.write(self.style.NOTICE(f'Started Crawling {i}'))
                    subprocess.run(["scrapy", "crawl", "konohagakure_to_be_crawled", "-a", f"allowed_domains={i.url}"], capture_output=False, check=True)
                    self.stdout.write(self.style.SUCCESS("Done"))
    
    @staticmethod
    def give_start_urls(domain: str):
        a=subprocess.run(["subfinder", "-d", domain], capture_output=True, check=True)
        return list(map(lambda a: f'https://{a}',str(a.stdout.decode()).strip().split('\n')))
    
    @staticmethod
    def find_subdomains(domain: str):
        a=subprocess.run(["subfinder", "-d", domain], capture_output=True, check=True)
        subdomains = list(map(lambda a: f'https://{a}',str(a.stdout.decode()).strip().split('\n')))
        for j in subdomains:
            try:
                a=ToBeCrawledWebPages(url=j,scan_internal_links=False)
                a.save()
            except:
                pass
        