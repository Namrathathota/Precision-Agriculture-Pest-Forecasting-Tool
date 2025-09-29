# Precision-Agriculture-Pest-Forecasting-Tool
🌾 A comprehensive tool that provides farmers with 24-72 hour forecast maps of likely pest infestation spread, enabling targeted drone-based spraying or manual intervention to save costs on pesticides and minimize environmental impact.

✨ Features
🔮 Advanced Forecasting

Multi-horizon predictions (24h, 48h, 72h)
Machine learning-powered pest movement models
Weather-integrated suitability analysis
Real-time risk assessment
🗺️ Interactive Visualizations

Dynamic heat maps of infestation probability
Timeline animations showing pest spread
Intervention planning maps with optimized routes
Mobile-friendly web interface
🌡️ Smart Weather Integration

Real-time weather data from OpenWeatherMap
Climate suitability calculations
Wind dispersal modeling
Demo mode available (no API key required)
🎯 Precision Interventions

Drone route optimization
Cost-effective treatment recommendations
Resource allocation strategies
Environmental impact minimization
🚀 Quick Start
Option 1: Demo Mode (Recommended for Testing)
# No API key required!
python main.py demo
Option 2: Web Application
python main.py web
# Open http://localhost:8501 in your browser
Option 3: Full Setup with Real Weather Data
Get free API key from OpenWeatherMap
Copy .env.example to .env and add your key
Run without demo mode
📋 Requirements
System Requirements:

Python 3.8+
Windows/Linux/macOS
2GB RAM minimum
Internet connection (for weather data)
Already Installed Dependencies:

✅ numpy, pandas, scikit-learn
✅ folium, geopandas (mapping)
✅ streamlit, flask (web interfaces)
✅ All other required packages
Installation
pip install -r requirements.txt
Usage
python main.py
Project Structure
pest/
├── src/
│   ├── data/
│   │   ├── weather_collector.py
│   │   ├── pest_data.py
│   │   └── field_data.py
│   ├── models/
│   │   ├── pest_movement.py
│   │   ├── weather_impact.py
│   │   └── risk_assessment.py
│   ├── mapping/
│   │   ├── visualization.py
│   │   ├── risk_overlay.py
│   │   └── route_optimizer.py
│   ├── prediction/
│   │   ├── forecast_engine.py
│   │   └── spread_calculator.py
│   └── web/
│       ├── app.py
│       ├── templates/
│       └── static/
├── data/
│   ├── sample_fields.geojson
│   └── pest_historical.csv
├── config/
│   └── settings.py
├── tests/
├── requirements.txt
└── main.py
API Keys
Configure your API keys in config/settings.py:

OpenWeatherMap API key
Any additional data sources
License
MIT License PS C:\Users\subha\Downloads\pest> C:/Users/subha/Downloads/pest/.venv/Scripts/python.exe main.py demo C:/Users/subha/Downloads/pest/.venv/Scripts/python.exe main.py webS
