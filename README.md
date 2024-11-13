# MQTT Data Simulator and PostgreSQL Migration Tool

This repository provides a simple simulator for creating and sending data over MQTT, then migrating the data to a PostgreSQL database for storage and analysis.

## Project Files

- **`mqtt_simulator.py`**: Simulates data generation and sends it via MQTT.
- **`mqtt_connector.py`**: Connects to the MQTT broker, retrieves data, and stores it in the PostgreSQL database.
- **`config.py`**: Holds configuration settings for the MQTT broker and PostgreSQL connection.

## Setup

1. **Install Requirements**  
   Ensure you have Python and the necessary libraries installed:
   ```bash
   pip install -r requirements.txt
