![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Kafka](https://img.shields.io/badge/Kafka-Event--Driven-orange)
# Smart-Air-Quality-Monitoring-System-Using-Cloud-Based-IoT-Simulation
> End-to-end simulation of a cloud-based IoT air quality monitoring pipeline using Kafka, PostgreSQL, and Streamlit.

This project simulates a cloud-based IoT system for real-time air quality monitoring **without using physical sensors**. It uses historical data and processes it through a cloud-inspired pipeline architecture using Kafka for communication between layers.

The system mimics how real IoT devices stream environmental data to the cloud for analysis and visualization.

---

## System Architecture  
Sensor Simulation → Kafka → Edge Processing → Cloud Storage → Streamlit Dashboard  

### 1. **Perception Layer (Sensor Simulation)**
- A Python script reads a historical dataset row-by-row.
- Data is sent to a Kafka topic (`air_quality_topic`) at fixed intervals (e.g., 1 second per row).

### 2. **Fog/Edge Layer (Preprocessing)**
- Reads data from Kafka.
- Filters out invalid values (e.g., negative readings).
- Adds an alert flag if PM2.5 exceeds a critical threshold (150 µg/m³).
- Forwards the processed data to a second topic (`processed_air_quality`).

### 3. **Cloud Layer (Storage & Ingestion)**
- Listens to the processed topic.
- Stores data into a PostgreSQL database (`airquality`, table: `air_data`).
- Acts as long-term storage for both historical analysis and real-time dashboards.

### 4. **Application Layer (Visualization)**
- Graphical dashboards will visualize:
  - Real-time values with alerts
  - Long-term averages, trends, and comparisons of various pollutant values
  - Interactable dashboard with several filters

---
## Screenshots

### Real-Time Data Visualization
<img src="visualization results/dashboard_pollutants.jpeg" width="700">

### Temperature & Humidty
<img src="visualization results/dashboard_tempereture.png" width="700">
---

## Tech Stack

| Layer            | Tools/Technologies                  |
|------------------|-------------------------------------|
| Simulation       | Python (pandas, kafka-python)       |
| Message Broker   | Apache Kafka (Docker)               |
| Edge Processing  | Python scripts                      |
| Cloud Storage    | PostgreSQL (Dockerized)             |
| Visualization    | Streamlit                           |

---

## Project Structure

```
├── data/
│   └── pollution.csv               # Raw dataset
│   └── clean_air_quality.csv       # Cleaned dataset with timestamps
├── prepare_data.py                 # Cleans dataset and adds timestamps
├── sensor_simulator.py             # Simulates IoT sensor data (Kafka Producer)
├── fog_processor.py                # Preprocesses data (Kafka Consumer → Producer)
├── cloud_consumer_postgres.py      # Stores processed data into PostgreSQL
├── dashboard.py                    # Streamlit visualization dashboard
├── docker-compose.yml              # Kafka, Zookeeper & PostgreSQL services
├── README.md                       # Project documentation
```

---

## Setup Instructions

### 1. Requirements

- Python ≥ 3.8
- Docker Desktop
- Postgres
- Python packages:

```bash
pip install pandas kafka-python psycopg2-binary
```

---

### 2. Start Docker Services

```bash
docker-compose up -d
```

This launches:
- Kafka
- Zookeeper
- PostgreSQL (with DB `airquality`)

---

### 3. Prepare the Dataset

```bash
python prepare_data.py
```

Cleans the raw dataset and generates `clean_air_quality.csv` with hourly timestamps.

---

### 4. Run the Simulation (in 3 separate terminals)

#### Terminal 1 – Simulated Sensor

```bash
python sensor_simulator.py
```

Sends one row of air quality data to Kafka every second.

#### Terminal 2 – Fog Layer Processor

```bash
python fog_processor.py
```

Filters the data, adds alerts, and sends it to a new topic.

#### Terminal 3 – Cloud Storage Consumer

```bash
python cloud_consumer_postgres.py
```

Stores the processed data into PostgreSQL.

---

### 5. Inspect the Database

Use **pgAdmin**, **DBeaver**, or any SQL client:

- Host: `localhost`
- Port: `5432`
- Username: `postgres`
- Password: `postgres`
- Database: `airquality`
- Table: `air_data`

---

## Visualization  
The dashboard is implemented using **Streamlit** and provides:

- **Real-time charts** (PM2.5, PM10, CO, Temperature, Humidity)
- **Alerts** when pollution exceeds thresholds
- **Historical trends** (daily averages, line graphs)

```bash
streamlit run dashboard.py
```

## Notes

- Kafka enables scalable, modular communication between components.
- PostgreSQL can be upgraded to **TimescaleDB** for better time-series performance.
- This is a fully local simulation of a cloud architecture.
- System designed to be **scalable, fault-tolerant**, and **reusable** in real deployments.

---

## Future Improvements

- Connect physical IoT sensors (e.g., with MQTT).
- Geo-based visualization on maps (leaflet / Mapbox).
- ML-based prediction and anomaly detection.
- Mobile client or web panel integration.

---

## Source Dataset

Air Quality & Pollution Dataset:  
https://www.kaggle.com/datasets/mujtabamatin/air-quality-and-pollution-assessment

---

**End-to-end cloud IoT simulation for air quality monitoring — from dataset to dashboard.**
