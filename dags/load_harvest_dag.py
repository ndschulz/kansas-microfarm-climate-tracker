from airflow.decorators import dag, task
from datetime import datetime, timedelta
import subprocess
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

default_args = {
    'owner': 'nickolas',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    dag_id='load_harvest_log',
    description='Load harvest log data into PostgreSQL',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=['harvest', 'microfarm']
)
def harvest_etl_pipeline():
    @task
    def run_harvest_script():
        subprocess.run(['python', 'load_harvest.py'], check=True)

    run_harvest_script()

harvest_etl_pipeline()
