import pendulum
from airflow.sdk.dag import dag
from airflow.sdk.task import task


@dag(
    dag_id='sample_pipeline',
    schedule='@daily',
    start_date=pendulum.datetime(2024, 1, 1, tz='UTC'),
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
