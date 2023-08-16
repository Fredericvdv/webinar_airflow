from datetime import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def print_message(**kwargs):
    # Extract the 'message' passed from the upstream DAG
    message = kwargs['dag_run'].conf.get('message')
    print(f"Upstream message: {message}")

# downstream DAG B
with DAG(
    dag_id="downstream_dag_B",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    schedule="@daily",
) as dag:
    downstream_task_B = PythonOperator(
        task_id="downstream_task_B",
        python_callable=print_message,
        provide_context=True  # This is necessary to access the dag_run conf in your callable
    )
