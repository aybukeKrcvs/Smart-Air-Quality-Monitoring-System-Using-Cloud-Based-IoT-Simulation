from kafka import KafkaConsumer, KafkaProducer
import json

# Kafka'dan gelen veriyi okuma (air_quality_topic)
consumer = KafkaConsumer(
    'air_quality_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='fog-layer-group'
)

# Kafka'ya işlenmiş veriyi yazma (processed_air_quality)
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Eşik değerler
PM25_THRESHOLD = 150

print("⏳ Fog Layer: Kafka'dan veri bekleniyor...\n")

for message in consumer:
    data = message.value

    # Negatif değer kontrolü
    if any([
        data.get("PM2.5", 0) < 0,
        data.get("PM10", 0) < 0,
        data.get("Temperature", 0) < -50,
        data.get("Humidity", 0) < 0,
    ]):
        print(f"❌ Hatalı veri atlandı: {data}")
        continue  # Bu veriyi geç

    # Hava kirliliği çok yüksekse uyarı bayrağı ekle
    if data.get("PM2.5", 0) > PM25_THRESHOLD:
        data["alert"] = True

    # Yeni topic'e gönder
    producer.send("processed_air_quality", data)
    print(f"✅ İşlenmiş veri gönderildi: {data['timestamp']}")

