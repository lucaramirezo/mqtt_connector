# Configuración del broker MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_USER = None  # Sin usuario y contraseña para pruebas locales
MQTT_PASSWORD = None
MQTT_CA_FILE = None  # No necesario pruebas locales

# Configuración de la base de datos PostgreSQL
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "postgres"  # !!
DB_USER = "postgres"
DB_PASSWORD = "Familiaramirez4"

# Lista de UUID válidos para testing
VALID_DEVICE_IDS = [
    "b834319d-42ec-4429-b687-1af98a7eb326",
    "f14a5840-75d3-47be-8dbe-6563ebe8b3d2",
    "6e554386-3b5e-4d5a-9f39-18f93870c4e0"
]

# Mapeo de data_type a type_code de sensor_data_type en DDBB
DATA_TYPE_MAP = {
    0x00: 'TMP',  # Temperature
    0x01: 'HMD',  # Humidity
    0x02: 'PRS',  # Pressure
    0x03: 'ACC',  # Acceleration
    0x04: 'GYR',  # Gyroscope
    0x05: 'MAG',  # Magnetometer
    0x06: 'LGT',  # Light Intensity
    0x07: 'PRX',  # Proximity
    0x08: 'ALT',  # Altitude
    0x09: 'VLT',  # Voltage
    0x0A: 'CUR',  # Current
    0x0B: 'SND',  # Sound Level
    0x0C: 'CO2',  # CO2 Level
    0x0D: 'PHL',  # pH Level
    0x0E: 'SPD',  # Speed
    0x0F: 'GPS',  # GPS Position
}
