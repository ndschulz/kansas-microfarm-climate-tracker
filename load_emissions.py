import os
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.dialects.postgresql import insert
from dotenv import load_dotenv
import logging
import sys

# Logging
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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

    logging.info("Reading emissions CSV...")
    df = pd.read_csv("emissions_log.csv")

    # Reflect emissions table from database
    metadata = MetaData()
    metadata.reflect(bind=engine)
    emissions_table = metadata.tables["emissions"]

    logging.info("Loading data to emissions table...")
    with engine.begin() as conn:
        for _, row in df.iterrows():
            stmt = insert(emissions_table).values(**row.to_dict())
            stmt = stmt.on_conflict_do_nothing(index_elements=["year", "county", "sector"])
            conn.execute(stmt)

    logging.info("Emissions data loaded successfully.")

except Exception as e:
    logging.error(f"Failed to load emissions data: {str(e)}")
    sys.exit(1)
