import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import logging
import sys

# Setup logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

try:
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    logging.info("Reading planting CSV...")
    df = pd.read_csv("plantings_log.csv")

    logging.info("Loading to plantings table...")
    df.to_sql("plantings", con=engine, if_exists="append", index=False)

    logging.info("Planting data loaded successfully.")

except Exception as e:
    logging.error(f"Failed to load planting data: {str(e)}")
    sys.exit(1)
