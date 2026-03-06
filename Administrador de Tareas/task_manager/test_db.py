from db import get_db_connection

try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE();")
    print("Conectado a la base:", cursor.fetchone())
    cursor.close()
    conn.close()
except Exception as e:
    print("Error de conexión:", e)