from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.sensors.external_task import ExternalTaskMarker

# upstream_dag_A
with DAG(
    dag_id="2_sensor_upstream_A",
    schedule='* * * * *',
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    
    start_task_A = BashOperator(
        task_id="start_task_A",
        bash_command="echo 'Start task in upstream_dag_A'",
    )
    
    end_task_A_marker = ExternalTaskMarker(
        task_id="end_task_A_marker",
        external_dag_id="2_sensor_downstream",
        external_task_id="sensor_A",
    )
    
    start_task_A >> end_task_A_marker


# upstream_dag_B
with DAG(
    dag_id="2_sensor_upstream_B",
    schedule='*/2 * * * *',
    # schedule='* * * * *',
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


# downstream_sensor_dag
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
        external_task_id="end_task_A_marker",
        timeout=60,                 # Time (in seconds) before the task times out and fails
        allowed_states=["success"],
    )

    sensor_B = ExternalTaskSensor(
        task_id="sensor_B",
        external_dag_id="2_sensor_upstream_B",
        external_task_id="end_task_B_marker",
        timeout=30,                 # in secondes
        allowed_states=["success"],
        execution_delta= timedelta(minutes=1)
    )
    
    start_task >> [sensor_A, sensor_B]