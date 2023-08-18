from datetime import datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.sensors.external_task_marker import ExternalTaskMarker

with DAG(
    dag_id="2_sensor_upstream_B",
    schedule='* * * * *',
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    
    start_task_B = BashOperator(
        task_id="start_task_B",
        bash_command="echo 'Start task in upstream_dag_B'",
    )
    
    end_task_B_marker = ExternalTaskMarker(
        task_id="end_task_B_marker",
        external_dag_id="downstream_sensor_dag",
        external_task_id="sensor_B",
    )
    
    start_task_B >> end_task_B_marker