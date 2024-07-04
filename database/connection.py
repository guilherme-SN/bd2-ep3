
import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="clinica_medica",
            user="root",
            password="root"
        )

        if connection.is_connected():
            return connection

        return None

    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None


def close_connection(connection, cursor=None):
    if connection:
        if cursor:
            cursor.close()
        connection.close()

