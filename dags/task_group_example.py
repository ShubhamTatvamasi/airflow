from datetime import datetime, timezone
from airflow.sdk import dag, task, TaskGroup

@dag(
    dag_id='task_group_example',
    schedule='@daily',
    start_date=datetime(2026, 3, 23, tzinfo=timezone.utc),
    catchup=False,
    tags=['example', 'task_group'],
)
def task_group_example():

    @task
    def start():
        print("Pipeline started")
        return {"batch_id": "batch_001"}

    @task
    def validate(data: dict):
        print(f"Validating batch: {data['batch_id']}")
        return data

    @task
    def extract_users(data: dict):
        print(f"Extracting users for {data['batch_id']}")
        return ["user_1", "user_2", "user_3"]

    @task
    def extract_orders(data: dict):
        print(f"Extracting orders for {data['batch_id']}")
        return ["order_1", "order_2"]

    @task
    def transform_users(users: list):
        print(f"Transforming {len(users)} users")
        return [u.upper() for u in users]

    @task
    def transform_orders(orders: list):
        print(f"Transforming {len(orders)} orders")
        return [o.upper() for o in orders]

    @task
    def load_users(users: list):
        print(f"Loading users: {users}")

    @task
    def load_orders(orders: list):
        print(f"Loading orders: {orders}")

    @task
    def finish():
        print("Pipeline complete")

    batch = start()
    validated = validate(batch)

    with TaskGroup("extract") as extract_group:
        users_raw = extract_users(validated)
        orders_raw = extract_orders(validated)

    with TaskGroup("transform") as transform_group:
        users_transformed = transform_users(users_raw)
        orders_transformed = transform_orders(orders_raw)

    with TaskGroup("load") as load_group:
        load_users(users_transformed)
        load_orders(orders_transformed)

    extract_group >> transform_group >> load_group >> finish()

task_group_example()
