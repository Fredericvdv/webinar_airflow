from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.python_operator import PythonOperator

# upstream DAG
with DAG(
  dag_id="upstream_dag",
  schedule="@daily",
  start_date=datetime(2023, 1, 1),
  catchup=False,
) as dag:
  start_task = BashOperator(
    task_id="start_task",
    bash_command="echo 'Start task'",
  )

  trigger_A = TriggerDagRunOperator(
    task_id="trigger_A",
    trigger_dag_id="1_downstream_dag_A",
    conf={"message":"Message to pass to downstream DAG A."},
  )

  trigger_B = TriggerDagRunOperator(
    task_id="trigger_B",
    trigger_dag_id="1_downstream_dag_B",
    conf={"message":"Message to pass to downstream DAG B."},
  )

  start_task >> trigger_A >> trigger_B


# downstream DAG A
with DAG(
  dag_id="downstream_dag_A",
  schedule="@daily",
  start_date=datetime(2023, 1, 1),
  catchup=False,
) as dag:
  downstream_task = BashOperator(
    task_id="downstream_task_A",
    bash_command='echo "Upstream message: $message"',
    env={"message": '{{ dag_run.conf.get("message") }}'},
  )


# downstream DAG B
def print_message(**kwargs):
    # Extract the 'message' passed from the upstream DAG
    message = kwargs['dag_run'].conf.get('message')
    print(f"Upstream message: {message}")

with DAG(
    dag_id="downstream_dag_B",
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    downstream_task_B = PythonOperator(
        task_id="downstream_task_B",
        python_callable=print_message,
        provide_context=True  # This is necessary to access the dag_run conf in your callable
    )