# fog_processor.py
from kafka import KafkaConsumer, KafkaProducer
import json

# Reading data from Kafka (air_quality_topic)
consumer = KafkaConsumer(
    'air_quality_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='fog-layer-group'
)

# Writing processed data to Kafka (processed_air_quality)
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Threshold values
PM25_THRESHOLD = 150

print("⏳ Fog Layer: Waiting for data from Kafka...\n")

for message in consumer:
    data = message.value

    # Negative value check
    if any([
        data.get("PM2.5", 0) < 0,
        data.get("PM10", 0) < 0,
        data.get("Temperature", 0) < -50,
        data.get("Humidity", 0) < 0,
    ]):
        print(f"❌ Invalid data skipped: {data}")
        continue  # Skip this data

    # If air pollution is very high, add an alert flag
    if data.get("PM2.5", 0) > PM25_THRESHOLD:
        data["alert"] = True

    # Send to new topic
    producer.send("processed_air_quality", data)
    print(f"✅ Processed data sent: {data['timestamp']}")