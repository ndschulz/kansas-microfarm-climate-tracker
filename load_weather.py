
import os
import requests
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.dialects.postgresql import insert
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
latitude = os.getenv("LAT")
longitude = os.getenv("LON")

# Create database engine
engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)

# Define historical date range
start_date = "2025-03-01"
end_date = datetime.today().strftime("%Y-%m-%d")

# Open-Meteo API URL
url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": start_date,
    "end_date": end_date,
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "weathercode",
        "apparent_temperature_max",
        "apparent_temperature_min"
    ],
    "temperature_unit": "fahrenheit",
    "precipitation_unit": "inch",
    "timezone": "auto"
}

response = requests.get(url, params=params)
print("Status Code:", response.status_code)
print("Response JSON:", response.json())


data = response.json()

daily = data["daily"]

# Weather code descriptions
weathercode_lookup = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Freezing rain: light",
    67: "Freezing rain: heavy",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

# Create DataFrame
df = pd.DataFrame({
    "date": daily["time"],
    "temp_max": daily["temperature_2m_max"],
    "temp_min": daily["temperature_2m_min"],
    "feels_like_max": daily["apparent_temperature_max"],
    "feels_like_min": daily["apparent_temperature_min"],
    "precipitation_in": daily["precipitation_sum"],
    "weather_code": daily["weathercode"]
})

# Map weather code to description
df["weather_description"] = df["weather_code"].map(weathercode_lookup)

# Load to Postgres (skip duplicates)
# Load to Postgres (skip duplicates by date)
with engine.begin() as conn:
    df.to_sql("weather", con=conn, index=False, if_exists="append", method="multi")


print("Weather data loaded successfully.")

# Placeholder for weather ETL script

