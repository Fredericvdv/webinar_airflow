from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.datasets import Dataset

dataset1 = Dataset('s3://folder1/dataset_1.txt')
dataset2 = Dataset('s3://folder1/dataset_2.txt')

# upstream A
with DAG(
    dag_id="4_dataset_upstream_A",
    schedule='* * * * *',
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    start_task = BashOperator(
        task_id="start_task",
        bash_command="echo 'Modify dataset_1.txt'",
        outlets=[dataset1],
    )

# upstream B
with DAG(
    dag_id="4_dataset_upstream_B",
    schedule='*/3 * * * *',
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    start_task = BashOperator(
        task_id="start_task",
        bash_command="echo 'Modify dataset_2.txt'",
        outlets=[dataset2],
    )

# downstream
with DAG(
    dag_id="4_dataset_downstream",
    schedule=[dataset1, dataset2],
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    start_task = BashOperator(
        task_id="start_task",
        bash_command="echo 'Start task'",
    )
    end_task = BashOperator(
        task_id="end_task",
        bash_command="echo 'End task'",
    )
    start_task >> end_task