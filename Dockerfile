FROM python:3.10.13

ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY=72b9416b80ab13391e2d5030938891b2dca2710b7e20635689e3aeff26d10f21
ENV AZURE_ACCOUNT_KEY=0T11+6nicayjPTdYFw76J7MBauIQFcPsl+y+b/jVV/MauVtXA93nbtMQwrbMkM9vBIPRjI2lMJqU+AStsRGjHw==
ENV AZURE_ACCOUNT_NAME=ferreteria
ENV AZURE_CONTAINER=mediastorage
ENV AZURE_MYSQL_HOST=adminferreteria-server.mysql.database.azure.com
ENV AZURE_MYSQL_NAME=adminferreteria-database
ENV AZURE_MYSQL_PASSWORD=31R6JVI14U4B8X44$
ENV AZURE_MYSQL_USER=wfgafucdpr
ENV WEBSITE_HOSTNAME=ferreteria-admin.azurewebsites.net

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

EXPOSE 8000

ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]