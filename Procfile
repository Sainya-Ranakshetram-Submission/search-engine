web: gunicorn search_engine.asgi:application -k search_engine.workers.DynamicUvicornWorker --timeout 500
worker: celery -A search_engine worker --loglevel=INFO
worker: celery -A search_engine beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
