# airflow

Install postgres:
```bash
helm upgrade -i postgres \
  oci://registry-1.docker.io/cloudpirates/postgres \
  --namespace airflow \
  --create-namespace \
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
  --set data.metadataConnection.host="postgres" \
  --set executor="CeleryExecutor"
```

Default login: `admin` / `admin`

---

Connect with postgres:
```bash
kubectl -n airflow exec -it postgres-0 -- sh -c \
  'PGPASSWORD=postgres psql -U postgres'
```

Check users list:
```sql
select * from ab_user;
```

---

Cleanup
```bash
helm un airflow postgres
kubectl delete ns airflow
```


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
