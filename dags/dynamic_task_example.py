from datetime import datetime, timezone
from airflow.sdk import dag, task

@dag(
    dag_id='dynamic_task_example',
    schedule='@daily',
    start_date=datetime(2026, 3, 23, tzinfo=timezone.utc),
    catchup=False,
    tags=['example', 'dynamic_task'],
)
def dynamic_task_example():

    @task
    def get_files() -> list[dict]:
        return [
            {"name": "sales_jan.csv", "size_mb": 10},
            {"name": "sales_feb.csv", "size_mb": 20},
            {"name": "sales_mar.csv", "size_mb": 15},
        ]

    @task
    def process_file(file: dict) -> dict:
        print(f"Processing {file['name']} ({file['size_mb']} MB)")
        return {"file": file["name"], "rows": file["size_mb"] * 1000}

    @task
    def summarize(results: list[dict]):
        total_rows = sum(r["rows"] for r in results)
        print(f"Processed {len(results)} files, {total_rows} total rows")

    files = get_files()
    results = process_file.expand(file=files)
    summarize(results)

dynamic_task_example()
