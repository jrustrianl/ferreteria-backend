FROM python:3.10.13-alpine3.18

ENV PYTHONUNBUFFERED 1

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app


ENTRYPOINT /app/manage.py runserver 0.0.0.0:80