# airflow

Install postgres:
```bash
helm upgrade -i postgres \
  oci://registry-1.docker.io/cloudpirates/postgres \
  --namespace airflow \
  --create-namespace \
  --set auth.password="postgres" \
  --wait \
  --timeout 10m
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
  --set airflowVersion="3.2.0" \
  --set defaultAirflowTag="3.2.0" \
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

Get inside `airflow-api-server` pod:
```bash
kubectl -n airflow \
  exec -it deploy/airflow-api-server -- bash
```

List all the DAGs:
```bash
airflow dags list
```

---

Cleanup
```bash
helm un airflow postgres
kubectl delete ns airflow
```

---

Add gitea remote repo
```bash
git remote add gitea http://10.10.10.8/admin/airflow.git
```

Push changes to gitea:
```bash
git push gitea main
```

