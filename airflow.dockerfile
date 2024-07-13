FROM apache/airflow:latest as airflow
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
WORKDIR /opt


COPY  requirement.txt .
USER airflow

RUN pip install -r requirement.txt --no-cache-dir
