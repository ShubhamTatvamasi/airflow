from datetime import datetime, timezone
from kubernetes.client import models as k8s
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.sdk import dag


@dag(
    dag_id="k8s_pod_custom_resources",
    start_date=datetime(2026, 6, 26, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
    tags=["kubernetes", "resources", "pod"],
)
def k8s_pod_custom_resources():
    light_task = KubernetesPodOperator(
        task_id="light_task",
        name="light-pod",
        namespace="airflow",
        image="python:3.14-slim",
        cmds=["python", "-c"],
        arguments=["""
            print("Light task: low resource usage")
        """],
        container_resources=k8s.V1ResourceRequirements(
            requests={"memory": "128Mi", "cpu": "100m"},
            limits={"memory": "256Mi", "cpu": "250m"},
        ),
        get_logs=True,
        is_delete_operator_pod=True,
        container_logs=True,
        in_cluster=True,
        termination_grace_period=30,
    )

    heavy_task = KubernetesPodOperator(
        task_id="heavy_task",
        name="heavy-pod",
        namespace="airflow",
        image="python:3.14-slim",
        cmds=["python", "-c"],
        arguments=["""
            import time
            print("Heavy task: high resource usage")
            data = list(range(10_000_000))
            print(f"Processed {len(data)} items")
        """],
        container_resources=k8s.V1ResourceRequirements(
            requests={"memory": "512Mi", "cpu": "500m"},
            limits={"memory": "1Gi", "cpu": "1"},
        ),
        get_logs=True,
        is_delete_operator_pod=True,
        container_logs=True,
        in_cluster=True,
        termination_grace_period=30,
    )

    light_task >> heavy_task


k8s_pod_custom_resources()
