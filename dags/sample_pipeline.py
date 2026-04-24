from datetime import datetime, timezone
from airflow.sdk import dag, task

@dag(
    dag_id='sample_pipeline',
    schedule='@daily',
    start_date=datetime(2026, 3, 24, tzinfo=timezone.utc),
    catchup=False,
    tags=['example', 'taskflow'],
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

sample_pipeline()
