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

