from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor

# downstream DAG
with DAG(
    dag_id="2_sensor_downstream",
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    start_task = BashOperator(
        task_id="start_task",
        bash_command="echo 'Start task'",
    )
    sensor_A = ExternalTaskSensor(
        task_id="sensor_A",
        external_dag_id="upstream_dag_A",
        external_task_id="end_task",
    )
    sensor_B = ExternalTaskSensor(
        task_id="sensor_B",
        external_dag_id="upstream_dag_B",
        external_task_id="start_task",
    )
    start_task >> sensor_A >> sensor_B