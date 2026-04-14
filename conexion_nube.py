import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        return mysql.connector.connect(
            host="sql10.freesqldatabase.com",
            user="sql10822747",
            password="eVJ7UCX6ZV",
            database="sql10822747",
            port=3306,
            connection_timeout=5
        )
    except Error as e:
        print("Error nube:", e)
        return None
