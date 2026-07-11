from datetime import datetime, timezone
from kubernetes.client import models as k8s
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.sdk import dag

PRINT_RESOURCES = """
import subprocess, os

def read_file(path):
    try:
        with open(path) as f:
            return f.read().strip()
    except Exception:
        return "unavailable"

# cgroup memory limit (what Kubernetes sets)
mem_limit_bytes = read_file("/sys/fs/cgroup/memory.max")
if mem_limit_bytes.isdigit():
    mem_limit_mb = int(mem_limit_bytes) / 1024 / 1024
    print(f"Memory limit (cgroup): {mem_limit_mb:.0f} Mi")
else:
    print(f"Memory limit (cgroup): {mem_limit_bytes}")

# current memory usage
mem_current = read_file("/sys/fs/cgroup/memory.current")
if mem_current.isdigit():
    mem_current_mb = int(mem_current) / 1024 / 1024
    print(f"Memory usage now:      {mem_current_mb:.1f} Mi")

# CPU quota (maps to CPU limit)
cpu_quota = read_file("/sys/fs/cgroup/cpu.max")
print(f"CPU quota (cgroup):    {cpu_quota}")

# number of CPUs visible
try:
    import multiprocessing
    print(f"CPU count visible:     {multiprocessing.cpu_count()}")
except Exception:
    pass

# downward API env vars if configured
for var in ["MY_CPU_REQUEST", "MY_MEM_REQUEST", "MY_CPU_LIMIT", "MY_MEM_LIMIT"]:
    val = os.environ.get(var)
    if val:
        print(f"{var}: {val}")
"""


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
        image="python:3.14-slim",
        cmds=["python", "-c"],
        arguments=[PRINT_RESOURCES + '\nprint("\\n--- light_task done ---")'],
        container_resources=k8s.V1ResourceRequirements(
            requests={"memory": "128Mi", "cpu": "100m"},
            limits={"memory": "256Mi", "cpu": "250m"},
        ),
        env_vars=[
            k8s.V1EnvVar(
                name="MY_CPU_REQUEST",
                value_from=k8s.V1EnvVarSource(
                    resource_field_ref=k8s.V1ResourceFieldSelector(
                        resource="requests.cpu", divisor="1m"
                    )
                ),
            ),
            k8s.V1EnvVar(
                name="MY_MEM_REQUEST",
                value_from=k8s.V1EnvVarSource(
                    resource_field_ref=k8s.V1ResourceFieldSelector(
                        resource="requests.memory", divisor="1Mi"
                    )
                ),
            ),
            k8s.V1EnvVar(
                name="MY_CPU_LIMIT",
                value_from=k8s.V1EnvVarSource(
                    resource_field_ref=k8s.V1ResourceFieldSelector(
                        resource="limits.cpu", divisor="1m"
                    )
                ),
            ),
            k8s.V1EnvVar(
                name="MY_MEM_LIMIT",
                value_from=k8s.V1EnvVarSource(
                    resource_field_ref=k8s.V1ResourceFieldSelector(
                        resource="limits.memory", divisor="1Mi"
                    )
                ),
            ),
        ],
        get_logs=True,
        is_delete_operator_pod=True,
        container_logs=True,
        in_cluster=True,
        termination_grace_period=30,
    )

    heavy_task = KubernetesPodOperator(
        task_id="heavy_task",
        name="heavy-pod",
        image="python:3.14-slim",
        cmds=["python", "-c"],
        arguments=[PRINT_RESOURCES + '\nprint("\\n--- heavy_task done ---")'],
        container_resources=k8s.V1ResourceRequirements(
            requests={"memory": "512Mi", "cpu": "500m"},
            limits={"memory": "1Gi", "cpu": "1"},
        ),
        env_vars=[
            k8s.V1EnvVar(
                name="MY_CPU_REQUEST",
                value_from=k8s.V1EnvVarSource(
                    resource_field_ref=k8s.V1ResourceFieldSelector(
                        resource="requests.cpu", divisor="1m"
                    )
                ),
            ),
            k8s.V1EnvVar(
                name="MY_MEM_REQUEST",
                value_from=k8s.V1EnvVarSource(
                    resource_field_ref=k8s.V1ResourceFieldSelector(
                        resource="requests.memory", divisor="1Mi"
                    )
                ),
            ),
            k8s.V1EnvVar(
                name="MY_CPU_LIMIT",
                value_from=k8s.V1EnvVarSource(
                    resource_field_ref=k8s.V1ResourceFieldSelector(
                        resource="limits.cpu", divisor="1m"
                    )
                ),
            ),
            k8s.V1EnvVar(
                name="MY_MEM_LIMIT",
                value_from=k8s.V1EnvVarSource(
                    resource_field_ref=k8s.V1ResourceFieldSelector(
                        resource="limits.memory", divisor="1Mi"
                    )
                ),
            ),
        ],
        get_logs=True,
        is_delete_operator_pod=True,
        container_logs=True,
        in_cluster=True,
        termination_grace_period=30,
    )

    light_task >> heavy_task


k8s_pod_custom_resources()
