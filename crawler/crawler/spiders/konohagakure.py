from __future__ import print_function     
from ctypes import *
from typing import List, Union, Optional
import scrapy
from crawler import standalone_django
from collections.abc import Iterable

lib = cdll.LoadLibrary("./subdomain_finder.so")
lib.Add.argtypes = [c_longlong, c_longlong]
lib.Add.restype = c_longlong

def get_all_subdomains() -> Iterable:
    for i in lib.find_subdomain(domain):
        yield i

class KonohagakureCrawler(scrapy.Spider):
    name : str = 'konohagakure'
    allowed_domains  = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        pass
