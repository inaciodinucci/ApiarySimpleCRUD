import os
from mysql.connector import connect, Error
from dotenv import load_dotenv

load_dotenv()

class DatabaseError(Exception):
    pass

def get_connection():
    try:
        connection = connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'apiario_db'),

        )
        return connection
    except Error as e:
        raise DatabaseError(f"Erro ao conectar ao banco de dados: {str(e)}")