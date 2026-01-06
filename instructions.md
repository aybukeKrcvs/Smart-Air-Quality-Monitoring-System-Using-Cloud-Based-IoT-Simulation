docker-compose up -d

docker-compose down --remove-orphans





**python sensor\_simulator.py**



**python fog\_processor.py**



**python cloud\_consumer\_postgres.py**



**http://localhost:3000/login**

**host.docker.internal:5432**

**airquality**

**postgres**

**postgres**

**SSL: disable**



**streamlit run dashboard.py**



**CREATE TABLE air\_data (**

    **timestamp TIMESTAMP PRIMARY KEY,**

    **pm25 FLOAT,**

    **pm10 FLOAT,**

    **temperature FLOAT,**

    **humidity FLOAT,**

    **so2 FLOAT,**

    **no2 FLOAT,**

    **co FLOAT,**

    **alert BOOLEAN**

**)**



**docker compose stop**

docker compose start

