import json
import paho.mqtt.client as mqtt
import random
import time
from config import MQTT_BROKER, MQTT_PORT, DATA_TYPE_MAP, VALID_DEVICE_IDS

TOPIC = "sensors/test"

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

client = mqtt.Client()
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
