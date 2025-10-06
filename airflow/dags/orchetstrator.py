HOST_PROJECT_PATH = '/home/noran/repos/weather-data-project'

from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
import sys
from airflow.providers.docker.operators.docker import DockerOperator 
from docker.types import Mount

sys.path.append('/opt/airflow/api-request')

def safe_main_callable():
    from insert_records import main
    return main()

default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(seconds=30),
}

dag = DAG(
    dag_id='weather-api-dbt-orchestrator',
    default_args=default_args,
    description='A DAG to orchestrate data',
    start_date=datetime(2025, 9, 27),
    schedule=timedelta(minutes=5),
    catchup=False
)

with dag:
    task1 = PythonOperator(
        task_id='ingest_data_task',
        python_callable=safe_main_callable
    )

    task2= DockerOperator(
        task_id='transform_data_task',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command = 'run',
        working_dir='/usr/app',

        mounts=[
            Mount(
                source=f'{HOST_PROJECT_PATH}/dbt/my_project',
                target='/usr/app',
                type='bind',
                read_only=False
            ),
            Mount(
                source=f'{HOST_PROJECT_PATH}/dbt/profiles.yml',
                target='/root/.dbt/profiles.yml',
                type='bind',
                read_only=True
            )
        ],
        
        network_mode='weather-data-project_my_network',
        docker_url='unix:///var/run/docker.sock',
        
        environment={
            'DBT_PROFILES_DIR': '/root/.dbt'
        },
        
        # Debugging
        auto_remove='success',
        retrieve_output=True,
        mount_tmp_dir=False,
    )



    task1 >> task2




    