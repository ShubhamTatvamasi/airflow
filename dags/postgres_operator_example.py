from datetime import datetime, timezone
from airflow.providers.postgres import PostgresOperator
from airflow.sdk import dag

@dag(
    dag_id='postgres_read_only_example',
    schedule=None,
    start_date=datetime(2026, 3, 24, tzinfo=timezone.utc),
    catchup=False,
    tags=['example', 'postgres', 'read-only'],
)

def postgres_read_only_example():
    query_airflow_metadata = PostgresOperator(
        task_id='query_airflow_metadata',
        postgres_conn_id='postgres_default',
        sql='SELECT id, dag_id, execution_date, state FROM dag_run ORDER BY execution_date DESC LIMIT 10;',
    )

    return query_airflow_metadata

dag = postgres_read_only_example()
