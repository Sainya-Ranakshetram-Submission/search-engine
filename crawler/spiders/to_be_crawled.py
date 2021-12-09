from __future__ import annotations

import os
from pathlib import Path

from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

dotenv_file = BASE_DIR / ".env"
if os.path.isfile(dotenv_file):
    import dj_database_url
    import django
    import dotenv
    dotenv.load_dotenv(dotenv_file)
    settings.configure(
        DATABASES={"default": dj_database_url.config(default=os.getenv("DATABASE_URL"))},
        INSTALLED_APPS=['main.apps.MainConfig'],
    )
    django.setup()
else:
    raise RuntimeError('DATABASE_URL is not set in environment variable')

import subprocess
from collections.abc import Iterable
from typing import List, Optional, Union
from scrapy.linkextractors import LinkExtractor

import nltk
import scrapy
import spacy
from django.utils.html import strip_tags
from main.models import CrawledWebPages, ToBeCrawledWebPages
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def give_start_urls(scan_internal_links: bool, domain: str):
    if scan_internal_links:
        a=subprocess.run(["subfinder", "-d", domain], capture_output=True)
        print(list(map(lambda a: f'https://{a}',str(a.stdout.decode()).strip().split('\n'))))
        return list(map(lambda a: f'https://{a}',str(a.stdout.decode()).strip().split('\n')))
    return [f'https://{domain}']

class KonohagakureCrawler(scrapy.Spider):
    name : str = 'konohagakure_to_be_crawled'
    
    def __init__(self, *args,**kwargs):
        self.allowed_domains: list = [kwargs.get('allowed_domains')]
        self.scan_internal_links: bool = True or kwargs.get('scan_internal_links')
        self.start_urls = give_start_urls(self.scan_internal_links, self.allowed_domains[0])
        if ToBeCrawledWebPages.objects.filter(url=self.allowed_domains[0]).exists():
            ToBeCrawledWebPages.objects.filter(url=self.allowed_domains[0]).delete()
        super().__init__(*args,**kwargs)

    def parse(self, response):
        if response.status == 200:
            if self.scan_internal_links:
                for link in LinkExtractor(deny_extensions=scrapy.linkextractors.IGNORED_EXTENSIONS).extract_links(response):
                    if not ToBeCrawledWebPages.objects.filter(url=link.url).exists():
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
            try:
                stripped_request_body=response.xpath("//meta[@name='description']/@content")[0].extract()
            except:
                stripped_request_body = None
            response.scan_internal_links = self.scan_internal_links
            if response.text:
                text = strip_tags(response.text)
                response_model.stripped_request_body = text[:250] or stripped_request_body
                nlp = spacy.load("en-core-web-md")
                doc = nlp(text)
                response_model.keywords_in_site = str(doc.ents)
                
                stop_words = set(stopwords.words('english'))
                tf_score = {}
                for each_word in total_words:
                    each_word = each_word.replace('.','')
                    if each_word not in stop_words:
                        if each_word in tf_score:
                            tf_score[each_word] += 1
                        else:
                            tf_score[each_word] = 1
                tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())
                response_model.keywords_ranking = tf_score
            response_model.save()
