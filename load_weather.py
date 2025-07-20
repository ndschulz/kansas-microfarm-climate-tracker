import os
import sys
import requests
import pandas as pd
import logging
from datetime import datetime, timedelta
from sqlalchemy import create_engine, MetaData
from sqlalchemy.dialects.postgresql import insert
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    logging.info("Starting WeatherAPI ETL...")

    # Config
    api_key = os.getenv("WEATHERAPI_KEY")
    location = "Lenexa,KS"
    start_date = datetime(2025, 3, 1).date()
    end_date = datetime.now().date()

    all_data = []

    for single_date in pd.date_range(start=start_date, end=end_date):
        date_str = single_date.strftime("%Y-%m-%d")
        url = f"http://api.weatherapi.com/v1/history.json?key={api_key}&q={location}&dt={date_str}"
        response = requests.get(url)
        logging.info(f"{date_str} - Status: {response.status_code}")
        if response.status_code != 200:
            logging.warning(f"Skipping {date_str} due to bad response.")
            continue

        json_data = response.json()
        try:
            day = json_data["forecast"]["forecastday"][0]["day"]
            all_data.append({
                "date": single_date.date(),
                "temp_max": day["maxtemp_f"],
                "temp_min": day["mintemp_f"],
                "temp_avg": day["avgtemp_f"],
                "precipitation_in": day["totalprecip_in"],
                "weather_code": None,
                "weather_description": day["condition"]["text"]
            })
        except (KeyError, IndexError) as e:
            logging.warning(f"Skipping {date_str} due to parsing error: {e}")
            continue

    df = pd.DataFrame(all_data)
    logging.info(f"Number of rows to insert: {len(df)}")
    if df.empty:
        raise ValueError("No weather data to insert. DataFrame is empty.")

    # DB connection
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "Nicksucks1")
    db_host = os.getenv("DB_HOST", "host.docker.internal")
    db_port = os.getenv("DB_PORT", "5433")
    db_name = os.getenv("DB_NAME", "microfarm")

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    metadata = MetaData()
    metadata.reflect(bind=engine)
    weather_table = metadata.tables["weather"]

    # Insert with conflict handling
    with engine.begin() as conn:
        for _, row in df.iterrows():
            stmt = insert(weather_table).values(**row.to_dict()).on_conflict_do_nothing(index_elements=["date"])
            result = conn.execute(stmt)
            #logging.info(f"Inserted row for {row['date']}: {result.rowcount} rows affected")

    logging.info("✅ Weather data loaded successfully from WeatherAPI.")

except Exception as e:
    logging.error(f"❌ WeatherAPI ETL failed: {e}")
    sys.exit(1)
