from datetime import datetime, timezone
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag

@dag(
    dag_id='bash_operator_example',
    schedule='@daily',
    start_date=datetime(2026, 3, 23, tzinfo=timezone.utc),
    catchup=False,
    tags=['example', 'bash'],
)

def bash_operator_example():
    print_date = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    sleep_task = BashOperator(
        task_id='sleep_task',
        bash_command='sleep 5',
    )

    completion = BashOperator(
        task_id='completion',
        bash_command='echo "BashOperator workflow complete"',
    )

    print_date >> sleep_task >> completion

dag = bash_operator_example()
