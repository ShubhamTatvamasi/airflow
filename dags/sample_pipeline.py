from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


# Task functions
def start_task():
    print("Starting the pipeline...")


def process_task():
    print("Processing data...")


def end_task():
    print("Pipeline completed.")


# DAG definition
with DAG(
    dag_id='sample_pipeline',
    default_args=default_args,
    description='A simple sample DAG',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:

    start = PythonOperator(
        task_id='start',
        python_callable=start_task,
    )

    process = PythonOperator(
        task_id='process',
        python_callable=process_task,
    )

    end = PythonOperator(
        task_id='end',
        python_callable=end_task,
    )

    # Task dependencies
    start >> process >> end
