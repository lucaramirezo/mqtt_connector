import psycopg2
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

try:
    print("Intentando conectar a la base de datos...")
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    print("Conexión a la base de datos establecida con éxito.")
    conn.close()
except Exception as e:
    print("Error al conectar a la base de datos:", e)
