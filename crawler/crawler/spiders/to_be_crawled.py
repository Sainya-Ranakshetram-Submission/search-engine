from __future__ import print_function     
from ctypes import *
from typing import List, Union, Optional
import scrapy
from crawler import standalone_django
from collections.abc import Iterable
from main.models import ToBeCrawledWebPages, CrawledWebPages
from django.utils.html import strip_tags
import spacy

lib = cdll.LoadLibrary("./subdomain_finder.so")
lib.Add.argtypes = [c_longlong, c_longlong]
lib.Add.restype = c_longlong

class KonohagakureCrawler(scrapy.Spider):
    name : str = 'konohagakure'
    allowed_domains: list
    start_urls = list(lib.find_subdomain(allowed_domains[0]))
    scan_internal_links: bool

    def parse(self, response):
        if response.status == 200:
            if self.scan_internal_links:
                for link in self.link_extractor.extract_links(response):
                    model = ToBeCrawledWebPages(url=link.url,scan_internal_links=False)
                    model.save()
            response_model = CrawledWebPages(
                url=response.url, 
                http_status=response.status,
                ip_address=response.ip_address,
                scan_internal_links=False,

            )
            try:
                keywords_meta_tags=response.xpath("//meta[@name='keywords']/@content")[0].extract()
                response_model.keywords_meta_tags=keywords_meta_tags
            except:
                pass
            if response.text:
                text = strip_tags(response.text)
                response_model.stripped_request_body = text
                nlp = spacy.load("en_core_web_sm")
                doc = nlp(text)
                keywords = doc.ents
                
            response_model.save()
        
        
        
