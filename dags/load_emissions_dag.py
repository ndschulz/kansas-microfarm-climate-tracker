from airflow.decorators import dag, task
from datetime import datetime, timedelta
import subprocess
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

default_args = {
    'owner': 'nickolas',
    'retries': 0,
    'retry_delay': timedelta(minutes=2),
}

@dag(
    dag_id='load_emissions_data',
    description='Load emissions data from CSV into PostgreSQL',
    schedule='@once',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=['emissions', 'microfarm']
)
def emissions_etl():
    @task
    def run_emissions_script():
        subprocess.run(['python', 'load_emissions.py'], check=True)

    run_emissions_script()

dag_instance = emissions_etl()
