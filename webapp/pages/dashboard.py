import sqlite3
import streamlit as st
import psutil
import time

from streamlit_autorefresh import st_autorefresh
import pandas as pd
import plotly.express as px


# Helper function
def get_system_health():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    uptime = time.time() - psutil.boot_time()
    return cpu_usage, memory_usage, uptime


# Function to get data from the database
@st.cache_data(ttl=60)  # Cache the data for 60 seconds
def refresh_data():
    conn = sqlite3.connect('databases/inference_data.db')
    
    query = "SELECT * FROM model_inference"
    data = pd.read_sql_query(query, conn)
    
    conn.close()
    return data

def show():
    # Fetch the data
    data = refresh_data()

    # User Overview
    st.title("📊 Dashboard")

    # Model Performance Metrics
    st.markdown("## 📈 Model Performance Metrics")
    col1, col2 = st.columns(2)
    col1.metric("Total Inferences", len(data))
    col2.metric("Average Inference Time (s)", data['inference_time'].mean())

    # Recent Interactions
    st.markdown("## 🕒 Recent Inferences")
    recent_data = data.sort_values(by='timestamp', ascending=False).head(10)
    st.dataframe(recent_data[['timestamp', 'model_name', 'inference_time', 'device']])

    # System Health Monitoring
    st.markdown("## 🖥️ System Health Monitoring")
    cpu_usage, memory_usage, uptime = get_system_health()
    col3, col4, col5 = st.columns(3)
    col3.metric("CPU Usage (%)", cpu_usage)
    col4.metric("Memory Usage (%)", memory_usage)
    col5.metric("Uptime (s)", uptime)

    # Visualize Inference Time Over Time
    st.markdown("## 📊 Inference Time Over Time")
    if not data.empty:
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        fig = px.line(data, x='timestamp', y='inference_time', title='Inference Time Over Time')
        st.plotly_chart(fig)

    # Auto-refresh control
    refresh_interval = st.slider("Select refresh interval in seconds", min_value=5, max_value=300, step=5, value=60)

    # Use st_autorefresh to automatically refresh the dashboard
    st_autorefresh(interval=refresh_interval * 1000)  # Convert seconds to milliseconds
