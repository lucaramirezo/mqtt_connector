import json
import paho.mqtt.client as mqtt
from DDBB import store_data_in_db
from config import MQTT_BROKER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD

# Función para manejar la conexión al broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT con éxito.")
        client.subscribe("sensors/test")  # Suscribirse al tema
    else:
        print(f"Error al conectar al broker MQTT. Código de retorno: {rc}")

# Función para manejar los mensajes recibidos
def on_message(client, userdata, msg):
    print("Mensaje recibido del broker MQTT.")  # Confirmar recepción del mensaje
    payload = msg.payload.decode()  # Decodificar el payload JSON

    try:
        # Cargar el JSON y extraer campos
        data = json.loads(payload)
        device_id = data['device_id']
        data_type = data['data_type']
        value = float(data['value'])  # Convertir el valor a float para el campo REAL en la base de datos

        print(f"Procesado - Device ID: {device_id}, Data Type: {data_type}, Value: {value}")

        # Almacenar en la base de datos
        store_data_in_db(device_id, data_type, value)
    except json.JSONDecodeError:
        print("Error al decodificar el mensaje JSON.")
    except KeyError as e:
        print(f"Falta el campo en el mensaje JSON: {e}")
    except Exception as e:
        print(f"Error al procesar el payload: {e}")

# Configuración y conexión al broker MQTT
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

try:
    print("Conectando al broker MQTT...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()
except Exception as e:
    print("Error al conectar al broker MQTT:", e)
