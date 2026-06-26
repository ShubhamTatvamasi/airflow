from datetime import datetime, timezone
from kubernetes.client import models as k8s
from airflow.sdk import dag, task


@dag(
    dag_id="custom_resources",
    start_date=datetime(2026, 6, 26, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
)
def custom_resources():
    @task(
        executor_config={
            "pod_override": k8s.V1Pod(
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name="base",
                            resources=k8s.V1ResourceRequirements(
                                requests={"memory": "128Mi", "cpu": "100m"},
                                limits={"memory": "256Mi", "cpu": "500m"},
                            ),
                        )
                    ]
                )
            )
        }
    )
    def run():
        import time
        print("running with custom resources")
        time.sleep(60)

    run()


custom_resources()
