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

---

Check the token:
```bash
echo $AIRFLOW_ACCESS_TOKEN
```

Check token details:
```
python3 - << EOF
import os
import json
import base64
from datetime import datetime

token = os.environ["AIRFLOW_ACCESS_TOKEN"]

payload = token.split(".")[1]
payload += "=" * (-len(payload) % 4)
claims = json.loads(base64.urlsafe_b64decode(payload))

exp = claims["exp"]
now = datetime.now().timestamp()
remaining = max(0, int(exp - now))

hours, remainder = divmod(remaining, 3600)
minutes, seconds = divmod(remainder, 60)

print(json.dumps(claims, indent=2))
print()
print(f"Expires at : {datetime.fromtimestamp(exp)}")
print(f"Time left  : {hours}h {minutes}m {seconds}s")
EOF
```
