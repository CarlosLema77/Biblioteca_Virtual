from config.database import get_database
from utils.mongo_helpers import parse_mongo_document


db = get_database()


def obtener_imagenes_libro(libro_id):
    imagenes = list(db.imagenes.find({"libro_id": libro_id}))
    return parse_mongo_document(imagenes)