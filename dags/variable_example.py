from datetime import datetime, timezone
from airflow.sdk import dag, task, Variable

@dag(
    dag_id='variable_example',
    schedule='@daily',
    start_date=datetime(2026, 3, 23, tzinfo=timezone.utc),
    catchup=False,
    tags=['example', 'variable'],
)
def variable_example():

    @task
    def print_environment():
        my_environment = Variable.get("my_environment")
        print(f"MY_ENVIRONMENT: {my_environment}")

        my_new_env = Variable.get("my_new_env")
        print(f"MY_NEW_ENV: {my_new_env}")

    print_environment()

variable_example()
