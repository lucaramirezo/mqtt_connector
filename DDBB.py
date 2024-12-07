import psycopg2
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def store_data_in_db(device_id, data_type, sensor_location, value):
    try:
        # Conexión a PostgreSQL
        print("Conectando a la base de datos PostgreSQL...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Inserción de datos en la tabla sensor_data_entry con valores por defecto para sub_type y sensor_location
        insert_query = """
        INSERT INTO neverasV1.sensor_data_entry (device_id, data_type, value, sub_type, sensor_location)
        VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (device_id, data_type, value, None, sensor_location))
        conn.commit()

        print("Datos insertados en la base de datos con éxito.")
    except Exception as e:
        print("Error al insertar datos en la base de datos:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("Conexión a la base de datos cerrada.")
