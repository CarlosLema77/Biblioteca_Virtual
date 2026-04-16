from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv
import os

load_dotenv()

class MongoDBConnection:
    """
    S: Solo maneja la conexión a MongoDB
    D: Expone get_database() como abstracción
    """
    
    def __init__(self):
        self._uri = os.getenv("MONGODB_URI")
        self._db_name = os.getenv("DB_NAME")
        self._client = None
        self._db = None

    def connect(self) -> Database:
        if self._client is None:
            self._client = MongoClient(self._uri)
            self._db = self._client[self._db_name]
        return self._db

    def get_database(self) -> Database:
        if self._db is None:
            return self.connect()
        return self._db

    def test_connection(self) -> bool:
        try:
            self._client.admin.command("ping")
            print("Conexión exitosa a MongoDB Atlas")
            print(f"Base de datos: {self._db_name}")
            return True
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False

# Instancia global — singleton
db_connection = MongoDBConnection()
db_connection.connect()

def get_database() -> Database:
    """Función de acceso global para el resto del proyecto"""
    return db_connection.get_database()


if __name__ == "__main__":
    db_connection.test_connection()