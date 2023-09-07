from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.sensors.external_task import ExternalTaskMarker

# ---------------------- UPSTREAM DAG A ---------------------- #
with DAG(
    dag_id="3_sensor_upstream_dag_A",
    schedule='*/3 * * * *',     # Runs every 3 minutes, starting at 0 minutes
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    
    start_task_A = BashOperator(
        task_id="start_task_A",
        bash_command="echo 'Start task in upstream_dag_A'",
    )
    
    end_task_A_marker = ExternalTaskMarker(
        task_id="end_task_A_marker",
        external_dag_id="3_sensor_downstream_dag",
        external_task_id="sensor_A",
    )
    
    start_task_A >> end_task_A_marker

# ---------------------- UPSTREAM DAG B ---------------------- #
with DAG(
    dag_id="3_sensor_upstream_dag_B",
    schedule='1-59/3 * * * *',   # Runs every 3 minutes, starting at 1 minute
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
        external_dag_id="3_sensor_downstream_dag",
        external_task_id="sensor_B",
    )
    
    start_task_B >> end_task_B_marker


# ---------------------- DOWNSTREAM DAG ---------------------- #
with DAG(
    dag_id="3_sensor_downstream_dag",
    schedule='2-59/3 * * * *',  # Runs every 3 minutes, starting at 2 minutes
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    
    start_task = BashOperator(
        task_id="start_task",
        bash_command="echo 'Start task'",
    )

    sensor_A = ExternalTaskSensor(
        task_id="sensor_A",
        external_dag_id="3_sensor_upstream_dag_A",
        external_task_id="end_task_A_marker",
        timeout=30,                 # Time (in seconds) before the task times out and fails
        allowed_states=["success"],
        execution_delta= timedelta(minutes=2)
    )

    sensor_B = ExternalTaskSensor(
        task_id="sensor_B",
        external_dag_id="3_sensor_upstream_dag_B",
        external_task_id="end_task_B_marker",
        timeout=30,                 
        allowed_states=["success"],
        execution_delta= timedelta(minutes=1)
    )
    
    start_task >> [sensor_A, sensor_B]