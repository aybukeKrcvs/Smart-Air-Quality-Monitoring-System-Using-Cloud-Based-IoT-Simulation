# cloud_consumer_postgres.py
from kafka import KafkaConsumer
import psycopg2
import json

# Kafka Consumer settings
consumer = KafkaConsumer(
    'processed_air_quality',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='cloud-postgres-group'
)

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="airquality",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

print("☁️ Cloud Layer (PostgreSQL): Waiting for data from Kafka...\n")

for msg in consumer:
    data = msg.value

    try:
        cursor.execute(
            """
            INSERT INTO air_data (timestamp, pm25, pm10, temperature, humidity, so2, no2, co, alert)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (timestamp) DO NOTHING;
            """,
            (
                data.get("timestamp"),
                float(data.get("PM2.5", 0)),
                float(data.get("PM10", 0)),
                float(data.get("Temperature", 0)),
                float(data.get("Humidity", 0)),
                float(data.get("SO2", 0)),
                float(data.get("NO2", 0)),
                float(data.get("CO", 0)),
                data.get("alert", False)
            )
        )
        conn.commit()
        print(f"✅ Written: {data['timestamp']}")
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()