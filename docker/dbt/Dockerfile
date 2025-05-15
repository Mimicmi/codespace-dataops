FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y build-essential libpq-dev git && \
    pip install --no-cache-dir dbt-postgres==1.4.0 pytz && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/app/dbt
