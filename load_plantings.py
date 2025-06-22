import os
import sys
import pandas as pd
import logging
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

try:
    logging.info("Starting planting ETL process...")

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    logging.info("Reading planting CSV...")
    df = pd.read_csv("planting_log.csv")

    logging.info("Loading to 'plantings' table...")
