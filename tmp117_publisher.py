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
        print("Error: No se pudo conectar al daemon de pigpio. ¿Está corriendo `sudo pigpiod`?")
        return

    # Configura el lector TMP117
    num_sensors = 3  # Cambiar al número real de sensores conectados
    locations = [f"lab_{i+1}" for i in range(num_sensors)]  # Define ubicaciones
    reader = TMP117Reader(pi, use_hardware=True)
    reader.setup_buses(num_sensors, locations)

    # Inicializa el cliente MQTT
    client = mqtt.Client()

    # Autenticación con usuario y contraseña
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

    # Configuración TLS/SSL si se proporciona un archivo CA
    if MQTT_CA_FILE:
        client.tls_set(MQTT_CA_FILE)

    try:
        # Conectar al broker MQTT
        client.connect(MQTT_BROKER, MQTT_PORT, 60)

        while True:
            for i, handler in enumerate(reader.i2c_handlers):
                try:
                    # Leer la temperatura del sensor
                    temperature = reader.read_temperature(handler)
                    if temperature is None:
                        raise ValueError("Datos no válidos")

                    # Crear payload JSON
                    payload = json.dumps({
                        "device_id": VALID_DEVICE_IDS[i % len(VALID_DEVICE_IDS)],  # UUID único por sensor
                        "data_type": "TMP",
                        "sensor_location": locations[i],
                        "value": round(temperature, 2)
                    })

                    # Publicar al broker MQTT
                    client.publish(TOPIC, payload)
                    print(f"Publicado: {payload}")

                except Exception as e:
                    print(f"Error al leer o publicar datos del sensor {i+1}: {e}")

            print("--------")
            time.sleep(1)  # Ajustar la frecuencia según sea necesario
    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
    finally:
        # Cerrar conexiones
        reader.close_buses()
        client.disconnect()
        pi.stop()

if __name__ == "__main__":
    main()
