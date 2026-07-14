# Variables and Connections

Check Database Connection:
```bash
airflow db check
```

### Import

Import variables:
```bash
airflow variables import variables.json
```

Import connections:
```bash
airflow connections import --overwrite connections.json
```

### Export


Export variables:
```bash
airflow variables export variables.json
```

Export connections:
```bash
airflow connections export connections.json
```

