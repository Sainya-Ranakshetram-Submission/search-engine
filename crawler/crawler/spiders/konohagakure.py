import scrapy
from crawler import standalone_django
from collections.abc import Iterable

def get_all_domains() -> Iterable:
    yield None

class KonohagakureCrawler(scrapy.Spider):
    name : str = 'konohagakure'
    allowed_domains  = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        pass
