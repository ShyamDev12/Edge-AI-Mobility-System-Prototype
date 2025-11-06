Edge AI Mobility System Prototype

A real-time Edge AI mobility monitoring dashboard built using Python and Streamlit, simulating intelligent fleet management through live telemetry, AI-based driver scoring, eco-efficiency, and actionable insights.

Overview

This project demonstrates how Edge AI can be used to improve:

Fleet safety through real-time driver behavior analysis

Routing efficiency and environmental impact

Emission monitoring and eco-driving insights

Driver experience through AI-powered recommendations

All processing happens in a local simulation (as a stand-in for on-vehicle edge nodes).

Key Features

Real-time vehicle telemetry simulation (speed, fuel rate, emissions)

AI-based driver scoring (lane discipline, drowsiness, overspeed)

Eco-driving score based on optimal performance parameters

Dynamic insights and recommendations using heuristic AI logic

Live map visualization for all active vehicles

Interactive charts for speed, fuel, and emission trends

Fully local and modular — extendable with actual ML models

Tech Stack

UI Dashboard: Streamlit
Data Processing: Pandas, NumPy
Simulation: Python Random module
AI Logic: Rule-based + expandable ML pipeline
Visualization: Streamlit Maps, Charts

System Flow

Edge Vehicle AI → Simulates telemetry data
Streamlit Backend → Aggregates, analyzes & visualizes
AI Insights UI → Driver scores, eco insights & alerts

Quick Start

Clone the repository:
git clone https://github.com/yourusername/edge-ai-mobility.git

cd edge-ai-mobility

Install dependencies:
pip install -r requirements.txt

Run the app:
streamlit run app.py

(Optional) Customize routes:
Edit or create routes.txt with your vehicle coordinates:
V001,12.9716,77.5946
V002,13.0321,77.5800
V003,12.9450,77.6200
