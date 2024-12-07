import json
import time
import random
import paho.mqtt.client as mqtt
from config import MQTT_BROKER, MQTT_PORT, VALID_DEVICE_IDS

TOPIC = "sensors/test"

# Simular datos de sensores TMP117
def simulate_sensor_data(sensor_id, location):
    """
    Genera datos simulados para un sensor TMP117.

    :param sensor_id: ID del sensor.
    :param location: Ubicación del sensor.
    :return: Payload JSON simulado.
    """
    return json.dumps({
        "device_id": random.choice(VALID_DEVICE_IDS),
        "data_type": "TMP",
        "sensor_location": location,
        "value": round(random.uniform(15.0, 20.0), 2)  # Temperatura simulada entre 15-20 °C
    })

def main():
    # Configuración de sensores simulados
    num_sensors = 5  # Número de sensores simulados
    locations = [f"lab_{i + 1}" for i in range(num_sensors)]

    # Inicializar el cliente MQTT
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    try:
        print("Iniciando simulación de sensores TMP117...")
        while True:
            for sensor_id, location in enumerate(locations, start=1):
                # Generar datos simulados
                payload = simulate_sensor_data(sensor_id, location)
                # Publicar al broker MQTT
                client.publish(TOPIC, payload)
                print(f"Publicado: {payload}")
            print("---- Ciclo de publicación completado ----")
            time.sleep(2)  # Pausa de 2 segundos entre ciclos (cambiar)
    except KeyboardInterrupt:
        print("Simulación interrumpida por el usuario.")
    finally:
        client.disconnect()
        print("Conexión MQTT cerrada.")

if __name__ == "__main__":
    main()
