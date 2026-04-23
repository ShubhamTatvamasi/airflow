from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime
from kubernetes.client import models as k8s

with DAG(
    dag_id="buildkit",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["docker", "buildkit"],
) as dag:

    build = KubernetesPodOperator(
        task_id="build_image",
        name="buildkit",
        namespace="airflow",
        in_cluster=True,

        image="moby/buildkit:latest",

        cmds=["/bin/sh", "-c"],
        arguments=["""
        buildctl-daemonless.sh build \
          --frontend dockerfile.v0 \
          --opt context=http://gitea-http.gitea/admin/airflow.git \
          --opt filename=docker/Dockerfile
        """],

        container_security_context=k8s.V1SecurityContext(
            privileged=True,
        ),

        get_logs=True,
        is_delete_operator_pod=True,
    )

    build
