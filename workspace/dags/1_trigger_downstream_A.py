from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

# downstream DAG A
with DAG(
  dag_id="downstream_dag_A",
  start_date=datetime(2023, 1, 1),
  catchup=False,
  schedule="@daily",
) as dag:
  downstream_task = BashOperator(
    task_id="downstream_task_A",
    bash_command='echo "Upstream message: $message"',
    env={"message": '{{ dag_run.conf.get("message") }}'},
)