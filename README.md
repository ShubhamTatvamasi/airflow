# airflow

Add airflow helm repo:
```bash
helm repo add airflow https://airflow.apache.org
```

Install airflow:
```bash
helm upgrade -i airflow airflow/airflow \
  --namespace airflow \
  --create-namespace \
  --set apiServer.service.type=LoadBalancer
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
