from datetime import datetime, timezone
from kubernetes.client import models as k8s
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.sdk import dag


@dag(
    dag_id="verify_resources",
    start_date=datetime(2026, 6, 26, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
)
def verify_resources():
    KubernetesPodOperator(
        task_id="verify",
        name="verify-resources-pod",
        namespace="airflow",
        image="python:3.14-slim",
        cmds=["sleep"],
        arguments=["60"],
        container_resources=k8s.V1ResourceRequirements(
            requests={"memory": "512Mi", "cpu": "250m"},
            limits={"memory": "2Gi", "cpu": "1"},
        ),
        get_logs=True,
        is_delete_operator_pod=True,
        in_cluster=True,
    )


verify_resources()
