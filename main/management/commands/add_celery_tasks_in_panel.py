"""
Add the celery tasks to the djangopanel
"""
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Command(BaseCommand):
    help = "Add the celery tasks to the django panel"
    requires_system_checks = output_transaction = True
        
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting"))
        try:
            IntervalSchedule.objects.update_or_create(every=12,period='hours')
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
        try:
            PeriodicTask.objects.update_or_create(
                name='crawl_already_crawled', 
                task='search_engine.celery.crawl_already_crawled',
                interval=IntervalSchedule.objects.filter(every=12,period='hours', ).all()[0],
                priority=1,
                start_time=now(),
                description='python manage.py crawl_already_crawled'
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
        try:
            PeriodicTask.objects.update_or_create(
                name='crawl_to_be_crawled', 
                task='search_engine.celery.crawl_to_be_crawled',
                interval=IntervalSchedule.objects.filter(every=12,period='hours', ).all()[0],
                priority=0,
                start_time=now(),
                description='python manage.py crawl_to_be_crawled'
            )
            self.stdout.write(self.style.NOTICE("Finished"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))