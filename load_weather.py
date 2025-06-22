import os
import sys
import requests
import pandas as pd
import logging
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    logging.info("Starting weather ETL process...")

    # Weathercode to description mapping
    weather_descriptions = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
        55: "Dense drizzle", 56: "Light freezing drizzle", 57: "Dense freezing drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain", 66: "Light freezing rain",
        67: "Heavy freezing rain", 71: "Slight snow fall", 73: "Moderate snow fall",
        75: "Heavy snow fall", 77: "Snow grains", 80: "Slight rain showers",
        81: "Moderate rain showers", 82: "Violent rain showers", 85: "Slight snow showers",
        86: "Heavy snow showers", 95: "Thunderstorm", 96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }

    # Set date range (backfill + forecast)
    end_date = datetime.now().date() + timedelta(days=7)
    start_date = datetime(2025, 3, 1).date()

    # Open-Meteo API parameters
    params = {
        "latitude": 38.9807,
        "longitude": -94.8082,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "apparent_temperature_max",
            "apparent_temperature_min",
            "precipitation_sum",
            "weathercode"
        ],
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
        "timezone": "America/Chicago",
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat()
    }

    response = requests.get("https://api.open-meteo.com/v1/forecast", params=params)
    logging.info(f"Weather API response code: {response.status_code}")
    data = response.json()

    # Convert to DataFrame
    df = pd.DataFrame({
        "date": data["daily"]["time"],
        "temp_max": data["daily"]["temperature_2m_max"],
        "temp_min": data["daily"]["temperature_2m_min"],
        "feels_like_max": data["daily"]["apparent_temperature_max"],
        "feels_like_min": data["daily"]["apparent_temperature_min"],
        "precipitation_in": data["daily"]["precipitation_sum"],
        "weather_code": data["daily"]["weathercode"]
    })

    # Add weather descriptions
    df["weather_description"] = df["weather_code"].map(weather_descriptions)
    df = df.dropna()
    df["date"] = pd.to_datetime(df["date"]).dt.date

    # Database connection
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
            conn.execute(stmt)

    logging.info("✅ Weather data loaded successfully.")

except Exception as e:
    logging.error(f"❌ Weather ETL failed: {e}")
    sys.exit(1)
