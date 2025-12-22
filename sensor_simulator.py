import pandas as pd
from kafka import KafkaProducer
import json
import time

# Veriyi oku
df = pd.read_csv("data/clean_air_quality.csv")

# Kafka Producer ayarı
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Her satırı Kafka topic'ine gönder
for index, row in df.iterrows():
    data = row.to_dict()
    producer.send('air_quality_topic', data)
    print(f"Gönderildi: {data['timestamp']}")
    time.sleep(1)  # 1 saniyede bir veri gönder

producer.flush()
producer.close()