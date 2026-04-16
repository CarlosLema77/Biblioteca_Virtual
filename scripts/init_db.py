"""
S: Solo se encarga de inicializar colecciones e índices
D: Depende de la abstracción get_database(), no del cliente directamente
"""

from pymongo import ASCENDING, TEXT
from pymongo.errors import CollectionInvalid
from config.database import get_database
from models.schemas import (
    SCHEMA_USUARIOS,
    SCHEMA_LIBROS,
    SCHEMA_AUTORES,
    SCHEMA_IMAGENES,
    SCHEMA_CHUNKS
)


def create_collection(db, name: str, schema: dict):
    """
    S: Solo crea una colección con su schema validation
    O: Acepta cualquier schema sin modificar la función
    """
    try:
        db.create_collection(name, validator=schema)
        print(f"Colección '{name}' creada")
    except CollectionInvalid:
        print(f"Colección '{name}' ya existe, omitiendo...")


def create_indexes(db):
    """
    S: Solo crea los índices del proyecto
    """
    print("\nCreando índices...")

    # Libros — índice compuesto fecha + idioma
    db["libros"].create_index(
        [("fecha_publicacion", ASCENDING), ("idioma", ASCENDING)],
        name="idx_fecha_idioma"
    )
    print("Índice compuesto: libros (fecha_publicacion, idioma)")

    # Libros — índice de texto
    db["libros"].create_index(
        [("titulo", TEXT), ("descripcion", TEXT)],
        name="idx_texto_libros"
    )
    print("Índice de texto: libros (titulo, descripcion)")

    # Chunks — índice compuesto para comparar estrategias
    db["chunks"].create_index(
        [("estrategia_chunking", ASCENDING), ("doc_id", ASCENDING)],
        name="idx_chunking_doc"
    )
    print("Índice compuesto: chunks (estrategia_chunking, doc_id)")

    # Usuarios — índice único en email
    db["usuarios"].create_index(
        [("email", ASCENDING)],
        unique=True,
        name="idx_email_usuario"
    )
    print("Índice único: usuarios (email)")


def init_database():
    """
    Función principal que orquesta la inicialización completa
    """
    print("Inicializando base de datos biblioteca_virtual...\n")
    
    db = get_database()

    # Crear colecciones
    print("Creando colecciones...")
    create_collection(db, "usuarios",  SCHEMA_USUARIOS)
    create_collection(db, "libros",    SCHEMA_LIBROS)
    create_collection(db, "autores",   SCHEMA_AUTORES)
    create_collection(db, "imagenes",  SCHEMA_IMAGENES)
    create_collection(db, "chunks",    SCHEMA_CHUNKS)

    # Crear índices
    create_indexes(db)

    print("\nBase de datos inicializada correctamente")


if __name__ == "__main__":
    init_database()