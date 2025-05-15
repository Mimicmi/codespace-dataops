FROM apache/airflow:2.5.0

USER root

RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip install great_expectations==0.15.46

USER airflow
