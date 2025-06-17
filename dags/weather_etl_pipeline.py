from airflow.decorators import dag, task
from datetime import datetime, timedelta
import subprocess
from dotenv import load_dotenv
import os

# Ensure .env loads even if working dir isn't root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

default_args = {
    'owner': 'nickolas',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    dag_id='load_weather_data',
    description='Load weather data from Open-Meteo API into PostgreSQL',
    schedule='0 11 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=['weather', 'microfarm']
)
def weather_etl_pipeline():
    @task
    def run_weather_script():
        subprocess.run(['python', 'load_weather.py'], check=True)

    run_weather_script()

dag_instance = weather_etl_pipeline()
