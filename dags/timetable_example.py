from datetime import datetime, timezone
from airflow.sdk import dag, task
from airflow.timetables.interval import CronDataIntervalTimetable

@dag(
    dag_id='timetable_example',
    # Run at 9 AM UTC on weekdays only (Mon-Fri)
    schedule=CronDataIntervalTimetable("0 9 * * 1-5", timezone="UTC"),
    start_date=datetime(2026, 3, 23, tzinfo=timezone.utc),
    catchup=False,
    tags=['example', 'timetable'],
)
def timetable_example():

    @task
    def extract(data_interval_start=None, data_interval_end=None):
        print(f"Extracting data for interval: {data_interval_start} -> {data_interval_end}")

    @task
    def transform(data_interval_start=None):
        print(f"Transforming data for: {data_interval_start}")

    @task
    def load(data_interval_start=None):
        print(f"Loading data for: {data_interval_start}")

    extract() >> transform() >> load()

timetable_example()
