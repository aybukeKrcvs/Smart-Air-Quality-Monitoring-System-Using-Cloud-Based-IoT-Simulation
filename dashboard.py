import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh

# ---------------- DB CONNECTION ----------------
def get_data():
    conn = psycopg2.connect(
        host="postgres",   # docker service name
        database="airquality",
        user="postgres",
        password="postgres"
    )
    query = """
    SELECT timestamp, pm25, pm10, no2, so2, co, temperature, humidity
    FROM air_data
    ORDER BY timestamp DESC
    LIMIT 500
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ---------------- STREAMLIT SETUP ----------------
st.set_page_config(page_title="Smart Air Quality Dashboard", layout="wide")
st.title("📡 Smart Air Quality Monitoring Dashboard")
st.markdown("Real-time visualization of pollutants and environmental parameters")

# 🔁 Auto refresh every 3 seconds
st_autorefresh(interval=3000, key="data_refresh")

df = get_data().sort_values("timestamp")

if df.empty:
    st.warning("No data found. Please ensure the simulation is running.")
    st.stop()

# ---------------- FILTERS ----------------
st.markdown("### 🔍 Data Filter")
min_date = df["timestamp"].min().date()
max_date = df["timestamp"].max().date()

start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01").date())
end_date = st.date_input("End Date", pd.to_datetime("2023-07-27").date())

filtered_df = df[
    (df["timestamp"].dt.date >= start_date) &
    (df["timestamp"].dt.date <= end_date)
]

# ---------------- KPI ----------------
st.markdown("### 🧪 Latest Sensor Readings")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

latest = df.iloc[-1]
kpi1.metric("PM2.5", f"{latest.pm25:.2f}")
kpi2.metric("PM10", f"{latest.pm10:.2f}")
kpi3.metric("NO2", f"{latest.no2:.2f}")
kpi4.metric("SO2", f"{latest.so2:.2f}")

# ---------------- POLLUTANT SELECTION ----------------
st.markdown("### 📌 Select Pollutants to Display")

options = {
    "pm25": {"label": "PM2.5", "color": "red", "threshold": 150},
    "pm10": {"label": "PM10", "color": "orange", "threshold": 100},
    "no2": {"label": "NO2", "color": "blue", "threshold": 75},
    "so2": {"label": "SO2", "color": "green", "threshold": 50},
    "co": {"label": "CO", "color": "purple", "threshold": 10}
}

selected = [
    key for key in options
    if st.checkbox(options[key]["label"], value=True, key=f"chk_{key}")
]

# ---------------- TIME SERIES ----------------
if selected:
    st.markdown("### 📈 Pollution Trends")

    fig = px.line(
        filtered_df,
        x="timestamp",
        y=selected,
        labels={"value": "Concentration (µg/m³)", "variable": "Pollutant"},
        title="Pollutant Levels Over Time"
    )

    for key in selected:
        fig.add_hline(
            y=options[key]["threshold"],
            line_dash="dash",
            line_color=options[key]["color"],
            annotation_text=f"{options[key]['label']} Threshold"
        )

    st.plotly_chart(fig, use_container_width=True, key="pollution_chart")

else:
    st.info("Please select at least one pollutant.")

# ---------------- TEMP & HUMIDITY ----------------
st.markdown("### 🌡️ Temperature and Humidity")
col1, col2 = st.columns(2)

with col1:
    st.line_chart(filtered_df.set_index("timestamp")["temperature"])

with col2:
    st.line_chart(filtered_df.set_index("timestamp")["humidity"])

# ---------------- CORRELATION ----------------
st.markdown("### 🔗 Correlation Matrix")
corr = filtered_df[["pm25","pm10","no2","so2","co","temperature","humidity"]].corr()

fig_corr, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig_corr)

