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

        cmds=["buildctl-daemonless.sh"],
        arguments=[
            "build",
            "--frontend=dockerfile.v0",
            "--opt", "context=http://gitea-http.gitea/admin/airflow.git#main:docker",

            # ✅ push image
            # "--output",
            # "type=image,name=your-dockerhub-username/your-image:latest,push=true",
        ],

        container_security_context=k8s.V1SecurityContext(
            privileged=True,
        ),

        # ✅ Docker auth secret
        # volumes=[
        #     k8s.V1Volume(
        #         name="docker-config",
        #         secret=k8s.V1SecretVolumeSource(
        #             secret_name="docker-config"
        #         ),
        #     )
        # ],
        # volume_mounts=[
        #     k8s.V1VolumeMount(
        #         name="docker-config",
        #         mount_path="/root/.docker"
        #     )
        # ],

        get_logs=True,
        is_delete_operator_pod=False,
    )

    build
