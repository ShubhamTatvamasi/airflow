# API

Generate Airflow Access Token:
```bash
export AIRFLOW_ACCESS_TOKEN=$(curl -sS \
  https://airflow.k8s.shubhamtatvamasi.com/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin"
  }' | jq -r '.access_token')
```

Check the token:
```bash
echo $AIRFLOW_ACCESS_TOKEN
```

```
python3 - << EOF
import os, json, base64

token = os.environ["AIRFLOW_ACCESS_TOKEN"]
payload = token.split(".")[1]
payload += "=" * (-len(payload) % 4)
print(json.dumps(json.loads(base64.urlsafe_b64decode(payload)), indent=2))
EOF
```



Trigger the DAG:
```bash
curl -sS -X POST \
  https://airflow.k8s.shubhamtatvamasi.com/api/v2/dags/bash_operator_example/dagRuns \
  -H "Authorization: Bearer $AIRFLOW_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"logical_date\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\"
  }" | jq
```
