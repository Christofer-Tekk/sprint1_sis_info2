import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="sql10.freesqldatabase.com",
        user="sql10822747",
        password="eVJ7UCX6ZV",
        database="sql10822747",
        port=3306
    )
