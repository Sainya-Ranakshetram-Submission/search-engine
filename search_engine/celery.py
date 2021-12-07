from __future__ import absolute_import

import os

from celery import Celery, shared_task
from celery.schedules import crontab
from django.conf import settings
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tgl.settings")

app = Celery("tgl", broker_url=settings.BROKER_URL)
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    "send-queued-mail": {
        "task": "post_office.tasks.send_queued_mail",
        "schedule": 60.0,
    },
    "send-queued-mail-main": {
        "task": "main.tasks.mail_queue",
        "schedule": 60.0,
    },
}