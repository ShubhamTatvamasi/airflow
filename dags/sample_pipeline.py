from datetime import datetime
from airflow.sdk import dag, task

@dag(
    dag_id='sample_pipeline',
    schedule='@daily',
    start_date=datetime(2026, 4, 24, tz='UTC'),
    catchup=False,
    tags=['example'],
)

def sample_pipeline():

    @task
    def start_task():
        print("Starting the pipeline...")

    @task
    def process_task():
        print("Processing data...")

    @task
    def end_task():
        print("Pipeline completed.")

    start = start_task()
    process = process_task()
    end = end_task()

    start >> process >> end

dag = sample_pipeline()
