import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

df = pd.read_csv("harvest_log.csv")

# Load to harvest_log table
with engine.begin() as conn:
    df.to_sql("harvest_log", con=conn, index=False, if_exists="append")

print("Harvest data loaded successfully.")
