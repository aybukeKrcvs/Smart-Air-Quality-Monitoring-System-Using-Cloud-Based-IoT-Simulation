import subprocess

subprocess.Popen(["python", "fog_processor.py"])
subprocess.Popen(["python", "cloud_consumer_postgres.py"])
subprocess.Popen(["python", "sensor_simulator.py"])
subprocess.Popen(["streamlit", "run", "dashboard.py"])