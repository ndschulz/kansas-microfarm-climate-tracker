# Kansas Micro-Farm Climate Tracker 🌱

This project is a comprehensive data pipeline and analytics system designed to help a small-scale Kansas micro-farm track and understand its local weather, planting, and harvest data over time. The system supports informed decision-making to optimize growing, track emissions, and understand the impact of climate variability on small-scale farming.

---

## 🚀 Overview

The Kansas Micro-Farm Climate Tracker collects, processes, and stores data in a PostgreSQL database and provides a foundation for building analytics and dashboards in Power BI or similar visualization tools.  

**Key features:**

- Automated daily weather data ingestion from Open-Meteo API
- Historical weather data backfilled
- Logging and tracking of planting and harvest activities
- Airflow-managed ETL pipelines
- Clean, modular Python code and reproducible data pipeline
- Emphasis on reproducibility and transparency

---

## 🗺️ Project Structure

\`\`\`
├── dags/
│   ├── load_weather_dag.py
│   ├── load_plantings_dag.py
│   ├── load_harvest_dag.py
├── load_weather.py
├── load_plantings.py
├── load_harvest.py
├── harvest_log.csv
├── plantings_log.csv
├── requirements.txt
├── README.md
└── .env
\`\`\`

---

## ⚡ Technologies Used

- **Python** (Pandas, SQLAlchemy, psycopg2)
- **Apache Airflow** (for scheduling and orchestration)
- **PostgreSQL** (data storage)
- **Docker** (local development environment)
- **Power BI** (for future dashboarding and analysis)
- **Open-Meteo API** (weather data source)

---

## 📊 Database Design

The PostgreSQL database includes the following core tables:

- **weather**: stores daily weather metrics (max temp, min temp, precipitation, etc.).
- **plantings**: logs planting activities, including bed, crop, planting date, expected harvest date.
- **harvest_log**: tracks harvested crops, weight, units, and bed location.
- **emissions**: (planned extension) tracks on-farm emissions and sustainability metrics.

---

## 🌀 ETL Pipeline

Airflow orchestrates three core pipelines:

1. **Weather ETL Pipeline**
   - Runs daily at 11:00 AM UTC
   - Fetches weather forecast and updates the database

2. **Plantings ETL Pipeline**
   - Loads new or updated planting records from \`plantings_log.csv\`

3. **Harvest ETL Pipeline**
   - Loads new harvest records from \`harvest_log.csv\`

---

## 🔥 Setup & Usage

### Prerequisites

- Docker
- Docker Compose (if used separately)
- PostgreSQL (local or Docker)
- Python 3.10+
- Airflow (running inside Docker using Astro CLI or similar)

---

### 1️⃣ Clone the repository

\`\`\`bash
git clone https://github.com/yourusername/kansas-microfarm-climate-tracker.git
cd kansas-microfarm-climate-tracker
\`\`\`

---

### 2️⃣ Configure environment

Create a \`.env\` file in the root directory:

\`\`\`
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=microfarm
POSTGRES_HOST=host.docker.internal
POSTGRES_PORT=5433
\`\`\`

Adjust values as needed for your setup.

---

### 3️⃣ Install dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

---

### 4️⃣ Start Airflow (example using Astro CLI)

\`\`\`bash
astro dev start
\`\`\`

Open Airflow UI at \`http://localhost:8080\`, enable and trigger DAGs as needed.

---

### 5️⃣ Load initial data

- Update \`plantings_log.csv\` and \`harvest_log.csv\` with your farm logs.
- Run the appropriate Airflow DAG or Python script manually:

\`\`\`bash
python load_plantings.py
python load_harvest.py
python load_weather.py
\`\`\`

---

## 🌽 How to Add New Plantings or Harvest

1. **Plantings**  
   - Update \`plantings_log.csv\` with new rows.
   - Run \`load_plantings.py\` or trigger the Airflow DAG.

2. **Harvest**  
   - Update \`harvest_log.csv\` with new records.
   - Run \`load_harvest.py\` or trigger the Airflow DAG.

---

## 🎯 Future Extensions

- Power BI dashboards for weather trends and yield analysis
- Emissions tracking and carbon footprint reporting
- Forecasting yields based on weather and planting data
- Automation of planting and harvest data entry via web UI
- Integration with IoT sensors for real-time field data

---

## 👨‍🌾 Author

**Nickolas Schulz**  
Data and Systems Analyst | Environmentalist | Builder of things that help communities thrive.

---

## 💬 Contributing

This is a personal portfolio project, but contributions, suggestions, or improvements are welcome. Please open an issue or create a pull request.

---

## ⚖️ License

This project is open source under the MIT License.

---

## 🌟 Acknowledgments

- Open-Meteo for providing free weather API access
- Airflow and the Astro community for making orchestration accessible
- Inspiration from the small farm and solarpunk community

---

*Happy growing! 🌱*
