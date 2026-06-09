from config.database import get_database
from bson import ObjectId
import os
from utils.mongo_helpers import serialize_doc

db = get_database()

def home():

    destacados = list(db.libros.find().limit(8))

    for libro in destacados:

        imagen = db.imagenes.find_one({
            "libro_id": libro["_id"]
        })

        if imagen and imagen.get("path_local"):

            filename = os.path.basename(imagen["path_local"])

            libro["imagen"] = f"http://localhost:8000/static/imagenes/{filename}"

        else:

            libro["imagen"] = "http://localhost:8000/static/imagenes/default-book.png"

    autores = list(db.autores.find().limit(6))
    generos = db.libros.distinct("genero")

    return serialize_doc({
        "destacados": destacados,
        "autores": autores,
        "generos": generos
    })