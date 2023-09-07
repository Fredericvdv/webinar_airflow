from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.python_operator import PythonOperator

# ---------------------- UPSTREAM DAG ---------------------- #
with DAG(
  dag_id="1_trigger_upstream_dag",
  schedule="@daily",
  start_date=datetime(2023, 1, 1),
  catchup=False,
  description="Upstream DAG that triggers downstream DAGs A and B",
) as dag:
  
  start_task = BashOperator(
    task_id="start_task",
    bash_command="echo 'Starting the upstream tasks!'",
  )

  trigger_A = TriggerDagRunOperator(
    task_id="trigger_A",
    trigger_dag_id="1_trigger_downstream_dag_A",
    conf={"message":"Message to pass to downstream DAG A."},
  )

  trigger_B = TriggerDagRunOperator(
    task_id="trigger_B",
    trigger_dag_id="1_trigger_downstream_dag_B",
    conf={"message":"Message to pass to downstream DAG B."},
  )

  start_task >> trigger_A >> trigger_B


# ---------------------- DOWNSTREAM DAG A ---------------------- #
with DAG(
  dag_id="1_trigger_downstream_dag_A",
  schedule=None,  # No need to schedule, it's triggered by upstream
  start_date=datetime(2023, 1, 1),
  catchup=False,
) as dag:
  
  downstream_task = BashOperator(
    task_id="downstream_task_A",
    bash_command='echo "Upstream message: $message"',
    env={"message": '{{ dag_run.conf.get("message") }}'},
  )


# ---------------------- DOWNSTREAM DAG B ---------------------- #
def print_message(**kwargs):
    # Extract the 'message' passed from the upstream DAG
    message = kwargs['dag_run'].conf.get('message')
    print(f"Received from upstream: {message}")

with DAG(
    dag_id="1_trigger_downstream_dag_B",
    schedule="@daily", # Also possible to schedule, but not necessary
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    
    downstream_task_B = PythonOperator(
        task_id="downstream_task_B",
        python_callable=print_message,
        provide_context=True  # This is necessary to access the dag_run conf in your callable
    )