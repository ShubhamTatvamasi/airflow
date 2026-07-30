# API

Generate Airflow Access Token:
```bash
AIRFLOW_ACCESS_TOKEN=$(curl --silent \
  https://airflow.k8s.shubhamtatvamasi.com/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin"
  }' | jq -r '.access_token')
```

