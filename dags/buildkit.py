from datetime import datetime, timezone
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.sdk import dag
from kubernetes.client import models as k8s

@dag(
    dag_id="buildkit",
    start_date=datetime(2026, 3, 23, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
    tags=["docker", "buildkit", "kubernetes", "pod"],
)
def buildkit():
    build = KubernetesPodOperator(
        task_id="build_image",
        name="buildkit",
        namespace="airflow",
        in_cluster=True,

        image="moby/buildkit:latest",

        cmds=["/bin/sh", "-c"],
        arguments=["""
            TARGET_SUCCESS=10
            success_count=0

            while [ "$success_count" -lt "$TARGET_SUCCESS" ]; do
                success_count=$((success_count + 1))

                wget -q -T 3 --tries=1 -O /dev/null https://registry-1.docker.io || true

                if buildctl-daemonless.sh build \
                    --frontend dockerfile.v0 \
                    --opt context=http://gitea-http.gitea/admin/airflow.git#:docker; then

                    echo "🎉 Build $success_count succeeded"

                    break
                fi

                echo "❌ Build $success_count failed"
            done
        """],

        container_security_context=k8s.V1SecurityContext(
            privileged=True,
        ),

        get_logs=True,
        is_delete_operator_pod=True,
    )

    return build

dag = buildkit()
