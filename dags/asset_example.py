from datetime import datetime, timezone
from airflow.sdk import dag, task, Asset

sales_asset = Asset("file://sales/daily.csv")
report_asset = Asset("file://reports/summary.csv")

@dag(
    dag_id='asset_producer',
    schedule='@daily',
    start_date=datetime(2026, 3, 23, tzinfo=timezone.utc),
    catchup=False,
    tags=['example', 'asset'],
)
def asset_producer():

    @task
    def extract() -> dict:
        print("Extracting raw sales data")
        return {"records": 1500, "date": "2026-03-23"}

    @task(outlets=[sales_asset])
    def load_sales(data: dict):
        print(f"Writing {data['records']} records to {sales_asset.name}")

    @task(outlets=[report_asset])
    def generate_report(data: dict):
        print(f"Generating summary report from {data['records']} records")

    data = extract()
    load_sales(data)
    generate_report(data)

asset_producer()


@dag(
    dag_id='asset_consumer',
    schedule=[sales_asset, report_asset],
    start_date=datetime(2026, 3, 23, tzinfo=timezone.utc),
    catchup=False,
    tags=['example', 'asset'],
)
def asset_consumer():

    @task
    def notify():
        print(f"Both assets are ready: {sales_asset.name}, {report_asset.name}")
        print("Running downstream pipeline")

    @task
    def archive():
        print("Archiving processed assets")

    notify() >> archive()

asset_consumer()
