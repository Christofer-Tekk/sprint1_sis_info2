import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="hospital_db",
            port=3306,
            use_pure=True   # 👈 🔥 IMPORTANTE
        )
        return conexion
    except Error as e:
        print("Error local:", e)
        return None
