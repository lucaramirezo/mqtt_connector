import json
import time
import paho.mqtt.client as mqtt
from tmp117_reader import TMP117Reader
import pigpio
from config import MQTT_BROKER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD, MQTT_CA_FILE, VALID_DEVICE_IDS

TOPIC = "sensors/test"  # Tópico para publicar los datos


def main():
    # Inicializa pigpio
    pi = pigpio.pi()
    if not pi.connected:
        print("Error: No se pudo conectar al daemon de pigpio.")
        return

    # Configura los buses y sus ubicaciones
    reader = TMP117Reader(pi, use_hardware=True)
    num_sensors = 2  # Número de sensores
    locations = [f"lab_{i+1}" for i in range(num_sensors)]
    reader.setup_buses(num_sensors, locations)

    # Configura MQTT
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    if MQTT_CA_FILE:
        client.tls_set(MQTT_CA_FILE)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    try:
        while True:
            for i, bus in enumerate(reader.buses):
                print(f"Bus {i}: SDA {bus['sda']}, SCL {bus['scl']}, Hardware: {bus['hardware']}")
                temperature = reader.read_temperature_from_bus(bus)
                if temperature is not None:
                    payload = json.dumps({
                        "device_id": VALID_DEVICE_IDS[i % len(VALID_DEVICE_IDS)],
                        "data_type": "TMP",
                        "sensor_location": locations[i],
                        "value": round(temperature, 2),
                    })
                    client.publish(TOPIC, payload)
                    print(f"Publicado: {payload}")
                else:
                    print(f"Error al leer sensor en {locations[i]}")
            print("--------")
            time.sleep(1)

    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
    finally:
        client.disconnect()
        pi.stop()


if __name__ == "__main__":
    main()
