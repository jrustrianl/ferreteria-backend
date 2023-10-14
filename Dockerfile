FROM python:3.10.13-alpine3.18

ENV PYTHONUNBUFFERED 1

WORKDIR /app
ADD . /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app


ENTRYPOINT FLASK_APP=/app/manage.py runserver 0.0.0.0:8000