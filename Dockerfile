FROM alpine:latest
FROM redis:apline
FROM postgres:alpine
FROM python:3-alpine
FROM golang:1.17-alpine
FROM rabbitmq:3.8-alpine

ENV POSTGRES_PASSWORD docker
ENV POSTGRES_DB search_engine
ENV DATABASE_URL postgres://postgres:docker@localhost:5432/search_engine
ENV LOGGING False

RUN apk add --no-cache --update redis:apline

WORKDIR /usr/src/app

COPY requirements.min.txt ./

RUN rabbitmq-plugins enable --offline rabbitmq_mqtt rabbitmq_federation_management rabbitmq_stomp
RUN pip install --no-cache-dir --upgrade -r requirements.min.txt
RUN python -m spacy download en_core_web_md
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader words
RUN go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
RUN pip install --upgrade django
RUN python manage.py migrate
RUN python manage.py collectcompress
RUN python manage.py add_celery_tasks_in_panel
RUN celery -A search_engine worker --loglevel=INFO
RUN celery -A search_engine beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

CMD ["uvicorn",  "manage.py", "search_engine.asgi:application", "--reload", "--lifespan", "off"]