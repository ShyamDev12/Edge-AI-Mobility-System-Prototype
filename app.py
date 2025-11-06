import streamlit as st
import pandas as pd
import numpy as np
import time
import random
from datetime import datetime

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Edge AI Mobility System Prototype", layout="wide")

st.title("🚗 Edge AI Mobility System Prototype")
st.caption("Simulated Edge AI Vehicles • Real-Time Telemetry • AI Insights")

# --------------------------------------------------
# INITIAL ROUTES
# --------------------------------------------------
ROUTE_FILE = "routes.txt"

@st.cache_data
def load_routes():
    routes = []
    try:
        with open(ROUTE_FILE, "r") as f:
            for line in f.readlines():
                if line.strip():
                    parts = line.strip().split(",")
                    routes.append({
                        "vehicle_id": parts[0],
                        "lat": float(parts[1]),
                        "lon": float(parts[2])
                    })
    except FileNotFoundError:
        # Default 3 vehicles if routes.txt missing
        routes = [
            {"vehicle_id": "V001", "lat": 12.9716, "lon": 77.5946},
            {"vehicle_id": "V002", "lat": 13.0321, "lon": 77.5800},
            {"vehicle_id": "V003", "lat": 12.9450, "lon": 77.6200}
        ]
    return routes

routes = load_routes()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "telemetry" not in st.session_state:
    st.session_state["telemetry"] = pd.DataFrame(columns=[
        "vehicle_id", "timestamp", "speed", "fuel_rate",
        "lane_departure", "driver_drowsy", "emission", "lat", "lon"
    ])

# --------------------------------------------------
# SIMULATION FUNCTION
# --------------------------------------------------
def simulate_vehicle_data(vehicle):
    """Simulates telemetry from an edge AI node"""
    return {
        "vehicle_id": vehicle["vehicle_id"],
        "timestamp": datetime.now(),
        "speed": random.uniform(20, 90),
        "fuel_rate": random.uniform(4, 12),
        "lane_departure": random.choice([True, False, False, False]),
        "driver_drowsy": random.choice([True, False, False, False, False]),
        "emission": random.uniform(100, 200),
        "lat": vehicle["lat"] + random.uniform(-0.002, 0.002),
        "lon": vehicle["lon"] + random.uniform(-0.002, 0.002)
    }

# --------------------------------------------------
# SIDEBAR CONTROLS
# --------------------------------------------------
st.sidebar.header("⚙️ Simulation Control")
refresh_rate = st.sidebar.slider("Refresh Interval (seconds)", 1, 5, 2)
num_points = st.sidebar.slider("Points to Display", 50, 300, 150)
show_alerts_only = st.sidebar.checkbox("Show Only Active Alerts", False)

# --------------------------------------------------
# LIVE DASHBOARD
# --------------------------------------------------
placeholder = st.empty()

while True:
    # Simulate new data
    new_data = [simulate_vehicle_data(v) for v in routes]
    new_df = pd.DataFrame(new_data)
    st.session_state["telemetry"] = pd.concat([
        st.session_state["telemetry"], new_df
    ]).tail(1000)

    telemetry = st.session_state["telemetry"].copy()
    telemetry["timestamp"] = pd.to_datetime(telemetry["timestamp"])

    # AI logic: compute driver score and eco score
    telemetry["driver_score"] = 100 - (
        telemetry["lane_departure"].astype(int)*20 +
        telemetry["driver_drowsy"].astype(int)*30 +
        (telemetry["speed"] > 80).astype(int)*10
    )

    telemetry["eco_score"] = np.clip(
        100 - ((telemetry["speed"] - 60).abs()/2 + telemetry["fuel_rate"]*2), 0, 100
    )

    # Layout
    with placeholder.container():
        col1, col2 = st.columns(2)

        # --- MAP VIEW ---
        with col1:
            st.subheader("📍 Fleet Map (Live)")
            map_df = telemetry.tail(len(routes))
            st.map(map_df.rename(columns={"lat": "latitude", "lon": "longitude"}))

        # --- TELEMETRY CHARTS ---
        with col2:
            st.subheader("📊 Telemetry Trends")
            st.line_chart(
                telemetry.set_index("timestamp")[["speed", "fuel_rate", "emission"]].tail(num_points)
            )

        # --- ALERTS ---
        st.divider()
        st.subheader("⚠️ Safety & Alerts")
        alerts = telemetry[
            (telemetry["lane_departure"]) | (telemetry["driver_drowsy"])
        ].sort_values("timestamp", ascending=False)

        if show_alerts_only:
            st.dataframe(alerts[["vehicle_id", "timestamp", "lane_departure", "driver_drowsy", "driver_score"]])
        else:
            st.dataframe(telemetry.tail(10)[
                ["vehicle_id", "timestamp", "speed", "fuel_rate", "emission", "driver_score", "eco_score"]
            ])

        # --- DRIVER SCORES ---
        st.divider()
        st.subheader("🧠 AI Scores Summary")
        avg_score = telemetry.groupby("vehicle_id")[["driver_score", "eco_score"]].mean().reset_index()
        st.bar_chart(avg_score.set_index("vehicle_id"))

        # --- AI RECOMMENDATIONS ---
        st.divider()
        st.subheader("🤖 AI Insights & Recommendations")

        insights = []
        for vid in avg_score["vehicle_id"]:
            ds = avg_score.loc[avg_score["vehicle_id"] == vid, "driver_score"].values[0]
            es = avg_score.loc[avg_score["vehicle_id"] == vid, "eco_score"].values[0]
            vdata = telemetry[telemetry["vehicle_id"] == vid]

            if ds < 70:
                insights.append(f"🚗 **{vid}**: Risky driving behavior detected — review lane discipline and fatigue.")
            if es < 60:
                insights.append(f"🌱 **{vid}**: Low eco-score — smoother acceleration or speed ≤ 65 km/h recommended.")
            if vdata["emission"].mean() > 180:
                insights.append(f"💨 **{vid}**: High emission level — check engine health or tire pressure.")
            if vdata["driver_drowsy"].any():
                insights.append(f"😴 **{vid}**: Driver fatigue signs detected — suggest rest break.")

        if len(insights) == 0:
            st.success("✅ All vehicles operating optimally. No active AI alerts.")
        else:
            for i in insights:
                st.info(i)

    # Refresh interval
    time.sleep(refresh_rate)
