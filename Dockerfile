FROM apache/airflow:3.3.0

RUN pip install \
    apache-airflow-providers-opensearch \
    apache-airflow-providers-postgres
