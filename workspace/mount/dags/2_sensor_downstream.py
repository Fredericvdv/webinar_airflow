from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor

with DAG(
    dag_id="2_sensor_downstream",
    schedule='* * * * *',
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    start_task = BashOperator(
        task_id="start_task",
        bash_command="echo 'Start task'",
    )
    sensor_A = ExternalTaskSensor(
        task_id="sensor_A",
        external_dag_id="2_sensor_upstream_A",
        external_task_id="end_task",
    )
    sensor_B = ExternalTaskSensor(
        task_id="sensor_B",
        external_dag_id="2_sensor_upstream_B",
        external_task_id="end_task_B_marker",
    )
    start_task >> sensor_A >> sensor_B