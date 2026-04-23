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
            success_count=0

            while [ "$success_count" -lt 5 ]; do
            echo "Attempt... success so far: $success_count"

            # Try registry check (but don't trust it fully)
            wget -q -T 3 --tries=1 -O /dev/null https://registry-1.docker.io
            wget_status=$?

            if [ "$wget_status" -ne 0 ]; then
                echo "⚠️ Registry check failed (continuing anyway)"
            else
                echo "✅ Registry reachable"
            fi

            # Always attempt build (this is what really matters)
            if buildctl-daemonless.sh build \
                --frontend dockerfile.v0 \
                --opt context=http://gitea-http.gitea/admin/airflow.git#:docker; then
                
                success_count=$((success_count + 1))
                echo "🎉 Build succeeded ($success_count/5)"
            else
                echo "❌ Build failed"
            fi

            sleep 2
            done

            echo "✅ Done: 5 successful builds completed"
        """],

        container_security_context=k8s.V1SecurityContext(
            privileged=True,
        ),

        get_logs=True,
        is_delete_operator_pod=True,
    )

    build
