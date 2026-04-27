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
        environment = Variable.get("environment")
        print(f"ENVIRONMENT: {environment}")

    print_environment()

variable_example()
