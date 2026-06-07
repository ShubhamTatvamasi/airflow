FROM apache/airflow:3.2.2

RUN pip install \
    apache-airflow-providers-opensearch \
    apache-airflow-providers-postgres
