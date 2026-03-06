import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="flask_user",       # Usuario que creaste
        password="MiContra123",  # Contraseña que pusiste
        database="task_manager"  # Base de datos
    )
    return conn