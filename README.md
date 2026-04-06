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
