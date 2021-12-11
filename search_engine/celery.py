from __future__ import absolute_import

import os
import subprocess

from celery import Celery, shared_task
from celery.schedules import crontab
from django.conf import settings
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "search_engine.settings")

app = Celery("search_engine", broker_url=settings.BROKER_URL)
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task
def crawl(domain: str):
    subprocess.run(["scrapy", "crawl", "konohagakure_to_be_crawled", "-a", f"allowed_domains={domain}"], capture_output=False)

@app.task
def find_subdomains(domain: str):
    try:
        if i.scan_internal_links:
            a=subprocess.run(["subfinder", "-d", domain], capture_output=True)
            subdomains = list(map(lambda a: f'https://{a}',str(a.stdout.decode()).strip().split('\n')))
            for j in subdomains:
                try:
                    a=ToBeCrawledWebPages(url=domain,scan_internal_links=False)
                    a.save()
                except:
                    pass
    except:
        pass