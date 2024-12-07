import json
import paho.mqtt.client as mqtt
import random
import time
from config import MQTT_BROKER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD, MQTT_CA_FILE, VALID_DEVICE_IDS, DATA_TYPE_MAP

TOPIC = "/test"

# Función para simular datos de sensores en JSON
def simulate_sensor_data():
    device_id = random.choice(VALID_DEVICE_IDS)  # Elegir un UUID válido aleatoriamente
    data_type = random.choice(list(DATA_TYPE_MAP.values()))  # Selecciona un tipo de dato aleatorio
    value = round(random.uniform(0, 100), 2)  # Genera un valor aleatorio como float

    # Crear mensaje JSON
    payload = json.dumps({
        "device_id": device_id,
        "data_type": data_type,
        "value": value
    })

    return payload

# Configuración del cliente MQTT
client = mqtt.Client()

# Autenticación con usuario y contraseña
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# Configuración del certificado CA para TLS/SSL
if MQTT_CA_FILE:
    client.tls_set(MQTT_CA_FILE)

# Conectar al broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

try:
    while True:
        payload = simulate_sensor_data()
        client.publish(TOPIC, payload)
        print("Mensaje enviado:", payload)
        time.sleep(1)
except KeyboardInterrupt:
    print("Simulador detenido.")
finally:
    client.disconnect()
