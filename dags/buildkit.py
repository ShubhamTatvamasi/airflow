import base64
import json
from datetime import datetime, timezone

from airflow.hooks.base import BaseHook
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.sdk import dag
from kubernetes.client import models as k8s

# Harbor connection (host + credentials) and target project.
HARBOR_CONN_ID = "my_harbor"
HARBOR_PROJECT = "airflow"
IMAGE_NAME = "app"
IMAGE_TAG = "latest"


def _harbor_config():
    """Resolve the Harbor registry host, image ref and a docker auth config
    from the my_harbor connection at parse time."""
    conn = BaseHook.get_connection(HARBOR_CONN_ID)

    # Registry host, e.g. "harbor.example.com" (strip any scheme).
    registry = conn.host or ""
    for scheme in ("https://", "http://"):
        if registry.startswith(scheme):
            registry = registry[len(scheme):]
    registry = registry.rstrip("/")

    image_ref = f"{registry}/{HARBOR_PROJECT}/{IMAGE_NAME}:{IMAGE_TAG}"

    auth = base64.b64encode(
        f"{conn.login}:{conn.password}".encode()
    ).decode()
    docker_config = json.dumps({"auths": {registry: {"auth": auth}}})

    return image_ref, docker_config


@dag(
    dag_id="buildkit",
    start_date=datetime(2026, 3, 23, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
    tags=["docker", "buildkit", "kubernetes", "pod", "harbor"],
)
def buildkit():
    image_ref, docker_config = _harbor_config()

    build = KubernetesPodOperator(
        task_id="build_image",
        name="buildkit",
        in_cluster=True,

        image="moby/buildkit:latest",

        # Provide registry credentials to buildkit via the docker config it
        # reads from ~/.docker/config.json.
        env_vars={"DOCKER_CONFIG": "/tmp/.docker"},

        cmds=["/bin/sh", "-c"],
        arguments=[f"""
            mkdir -p /tmp/.docker
            printf '%s' '{docker_config}' > /tmp/.docker/config.json

            buildctl-daemonless.sh build \
                --frontend dockerfile.v0 \
                --opt context=https://github.com/ShubhamTatvamasi/airflow.git#:docker \
                --output type=image,name={image_ref},push=true
        """],

        container_security_context=k8s.V1SecurityContext(
            privileged=True,
        ),

        get_logs=True,
        is_delete_operator_pod=True,
    )

    return build

buildkit()
