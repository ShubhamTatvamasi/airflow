# airflow

Install postgres:
```bash
helm upgrade -i postgres \
  --namespace airflow \
  --create-namespace \
  oci://registry-1.docker.io/cloudpirates/postgres \
  --set auth.password="postgres"
```

Add airflow helm repo:
```bash
helm repo add airflow https://airflow.apache.org
```

Install airflow:
```bash
helm upgrade -i airflow airflow/airflow \
  --namespace airflow \
  --create-namespace \
  --set postgresql.enabled=false \
  --set apiServer.service.type=LoadBalancer \
  --set data.metadataConnection.host="postgres-postgres" \
  --set executor="CeleryExecutor"
```

Default login: `admin` / `admin`

---

Get inside `airflow-api-server` pod:
```bash
kubectl -n airflow \
  exec -it deploy/airflow-api-server -- bash
```

List all the DAGs:
```bash
airflow dags list
```
