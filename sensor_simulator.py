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
    data = row.to_dict()
    producer.send('air_quality_topic', data)
    print(f"Sent: {data['timestamp']}")
    time.sleep(1)  # Send data every 1 second

producer.flush()
producer.close()