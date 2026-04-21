from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime

with DAG(
    dag_id="python_slim_k8s_pod",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["kubernetes", "python-slim"],
) as dag:

    run_python = KubernetesPodOperator(
        task_id="run_python_script",

        name="python-slim-pod",
        namespace="default",  # change if needed

        image="python:3.14-slim",

        cmds=["python", "-c"],
        arguments=[
            """
import datetime
print("Hello from python:slim container")
print("Current time:", datetime.datetime.now())
"""
        ],

        get_logs=True,
        is_delete_operator_pod=True,

        in_cluster=True,  # True if Airflow is running inside K8s
        termination_grace_period=30,
    )

    run_python
