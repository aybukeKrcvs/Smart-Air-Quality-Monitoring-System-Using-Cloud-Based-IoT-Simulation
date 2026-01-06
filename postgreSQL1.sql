CREATE TABLE air_data (
    timestamp TIMESTAMP PRIMARY KEY,
    pm25 FLOAT,
    pm10 FLOAT,
    temperature FLOAT,
    humidity FLOAT,
    co FLOAT,
    so2 FLOAT,
    no2 FLOAT,
    alert BOOLEAN
);