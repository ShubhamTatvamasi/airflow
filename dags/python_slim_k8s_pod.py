from datetime import datetime, timezone
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.sdk import dag

@dag(
    dag_id="python_slim_k8s_pod",
    start_date=datetime(2026, 3, 23, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
    tags=["kubernetes", "python-slim", "pod"],
)

def python_slim_k8s_pod():
    run_python = KubernetesPodOperator(
        task_id="run_python_script",

        name="python-slim-pod",
        namespace="airflow",

        image="python:3.14-slim",

        cmds=["python", "-c"],
        arguments=["""
            import datetime
            print("Hello from python:slim container")
            print("Current time:", datetime.datetime.now())
        """],

        get_logs=True,
        is_delete_operator_pod=True,
        container_logs=True,

        in_cluster=True,
        termination_grace_period=30,
    )

    return run_python

dag = python_slim_k8s_pod()
