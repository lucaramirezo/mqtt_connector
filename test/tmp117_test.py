import json
import time
import random
import paho.mqtt.client as mqtt
from tmp117_reader import TMP117Reader
import pigpio
from config import MQTT_BROKER, MQTT_PORT, VALID_DEVICE_IDS

TOPIC = "sensors/test"  # Tópico de prueba

# Simular TMP117 para testing (si no están físicamente conectados)
def simulate_tmp117_data(sensor_id, location):
    """
    Genera datos simulados para un sensor TMP117.

    :param sensor_id: ID del sensor.
    :param location: Ubicación del sensor.
    :return: Payload JSON simulado.
    """
    return json.dumps({
        "device_id": random.choice(VALID_DEVICE_IDS),  # UUID válido aleatorio
        "data_type": "temperature",
        "sensor_location": location,
        "value": round(random.uniform(15.0, 20.0), 2)  # Simula una temperatura entre 15 y 20 °C
    })

def main():
    # Inicializa pigpio y configura los sensores reales
    pi = pigpio.pi()
    if not pi.connected:
        print("Error: No se pudo conectar al daemon de pigpio")
        return

    # Configura el lector TMP117
    num_sensors = 3  # Cambiar al número real de sensores conectados
    locations = [f"lab_{i+1}" for i in range(num_sensors)]  # Define ubicaciones de prueba
    reader = TMP117Reader(pi, use_hardware=True)
    reader.setup_buses(num_sensors, locations)

    # Inicializa el cliente MQTT
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    try:
        while True:
            for i, handler in enumerate(reader.i2c_handlers):
                # Intenta leer datos reales o genera simulados si no está conectados
                try:
                    temperature = reader.read_temperature(handler)
                    if temperature is None:
                        raise ValueError("Datos no válidos")
                    payload = json.dumps({
                        "device_id": random.choice(VALID_DEVICE_IDS),  # UUID válido aleatorio
                        "data_type": "temperature",
                        "sensor_location": locations[i],
                        "value": round(temperature, 2)
                    })
                except Exception:
                    payload = simulate_tmp117_data(i + 1, locations[i])

                # Publica los datos al broker MQTT
                client.publish(TOPIC, payload)
                print(f"Publicado: {payload}")
            print("--------")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
    finally:
        # Cierra las conexiones
        reader.close_buses()
        client.disconnect()
        pi.stop()

if __name__ == "__main__":
    main()
