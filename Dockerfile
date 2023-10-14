FROM python:3.10.13-alpine3.18

ENV PYTHONUNBUFFERED 1

RUN apt-get install -y libmysqlclient-dev
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT /app/manage.py runserver 0.0.0.0:80