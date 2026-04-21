from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime

from kubernetes.client import models as k8s

with DAG(
    dag_id="rootless_buildkit",
    start_date=datetime(2024, 1, 1),
    schedule=None,  # ✅ Airflow 3 change
    catchup=False,
    tags=["docker", "buildkit"],
) as dag:

    build = KubernetesPodOperator(
        task_id="build_image",
        name="rootless-buildkit",
        namespace="default",

        image="moby/buildkit:rootless",

        cmds=["buildctl-daemonless.sh"],
        arguments=[
            "build",
            "--frontend=dockerfile.v0",

            # ✅ Use Git context (VERY IMPORTANT)
            "--opt", "context=http://gitea-http.gitea/admin/airflow.git",
            "--opt", "dockerfile=docker/Dockerfile",
            # "--opt", "subdir=docker",

            # ✅ push image
            # "--output",
            # "type=image,name=your-dockerhub-username/your-image:latest,push=true",
        ],

        # ✅ Required for rootless buildkit in many clusters
        env_vars={
            "BUILDKITD_FLAGS": "--oci-worker-no-process-sandbox"
        },

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

        # ✅ good practice
        # is_delete_operator_pod=True,
        get_logs=False,

        # ✅ Airflow 3 / K8s stability
        # container_resources=k8s.V1ResourceRequirements(
        #     requests={"cpu": "500m", "memory": "512Mi"},
        #     limits={"cpu": "1", "memory": "1Gi"},
        # ),
    )

    build
