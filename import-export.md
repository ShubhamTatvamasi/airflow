# Variables and Connections

Check Database Connection:
```bash
airflow db check
```

### Import

Import variables:
```bash
airflow variables import variables.yaml
```

Import connections:
```bash
airflow connections import --overwrite connections.yaml
```

### Export


Export variables:
```bash
airflow variables export variables.yaml
```

Export connections:
```bash
airflow connections export connections.yaml
```

---

Convert json to yaml
```bash
cat variables.json | yq -P > variables.yaml
```

---

### Export Airflow 2

Export connections:
```bash
airflow connections export \
  --file-format yaml \
  connections.yaml
```



