from datetime import datetime, timezone
from airflow.sdk import dag, task

@dag(
    dag_id='xcom_example',
    schedule='@daily',
    start_date=datetime(2026, 3, 23, tzinfo=timezone.utc),
    catchup=False,
    tags=['example', 'xcom'],
)
def xcom_example():

    @task
    def extract():
        data = {"name": "airflow", "version": 3}
        return data  # return value is automatically pushed to XCom

    @task
    def transform(raw: dict):
        raw["name"] = raw["name"].upper()
        return raw

    @task
    def load(processed: dict):
        print(f"Loading: {processed}")

    raw = extract()
    transformed = transform(raw)
    load(transformed)

xcom_example()
