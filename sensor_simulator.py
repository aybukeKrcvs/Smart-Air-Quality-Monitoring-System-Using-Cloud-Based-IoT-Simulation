# sensor_simulator.py
import pandas as pd
from kafka import KafkaProducer
import json
import time

# Read cleaned data
df = pd.read_csv("data/clean_air_quality.csv")

# Kafka Producer settings
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send each row to Kafka topic
for index, row in df.iterrows():
    data = {
        "timestamp": row["timestamp"],
        "PM2.5": row["PM2.5"],
        "PM10": row["PM10"],
        "Temperature": row["Temperature"],
        "Humidity": row["Humidity"],
        "CO": row["CO"],
        "SO2": row["SO2"],
        "NO2": row["NO2"]
    }
    producer.send('air_quality_topic', data)
    print(f"Send: {data['timestamp']}")
    time.sleep(3)

producer.flush()
producer.close()