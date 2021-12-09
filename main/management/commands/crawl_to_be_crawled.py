"""
 Scraping newly entered sites in database
"""

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from main.models import ToBeCrawledWebPages
import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from crawler.crawler.spiders import to_be_crawled


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
        runner = CrawlerRunner({'USER_AGENT': return_random_user_agent(),'allowed_domains':['fateslist.xyz']})
        d = runner.crawl(to_be_crawled.KonohagakureCrawler)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
        
        