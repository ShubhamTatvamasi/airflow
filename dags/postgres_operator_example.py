from datetime import datetime, timezone
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk import dag

@dag(
    dag_id='postgres_read_only_example',
    schedule=None,
    start_date=datetime(2026, 3, 24, tzinfo=timezone.utc),
    catchup=False,
    tags=['example', 'postgres', 'read-only'],
)

def postgres_read_only_example():
    query_airflow_metadata = SQLExecuteQueryOperator(
        task_id='query_airflow_metadata',
        conn_id='postgres_default',
        sql='SELECT id, dag_id, logical_date, state FROM dag_run ORDER BY logical_date DESC LIMIT 10;',
    )

    return query_airflow_metadata

dag = postgres_read_only_example()
