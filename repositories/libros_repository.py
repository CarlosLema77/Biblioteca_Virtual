from config.database import get_database
from bson import ObjectId
import os
from utils.mongo_helpers import parse_mongo_document

db = get_database()


def get_all_books():
    libros = list(db.libros.find())
    return parse_mongo_document(libros)


def get_book_by_id(book_id):
    libro = db.libros.find_one({"_id": ObjectId(book_id)})
    return parse_mongo_document(libro)


def get_books_by_author(author_id):
    libros = list(db.libros.find({"autor_id": ObjectId(author_id)}))
    return parse_mongo_document(libros)


def get_books_by_genre(genero):
    libros = list(db.libros.find({"genero": genero}))
    return parse_mongo_document(libros)


def get_featured_books(limit=8):
    libros = list(db.libros.find().limit(limit))
    return parse_mongo_document(libros)


def get_complete_book(id):
    libro = db.libros.find_one({"_id": ObjectId(id)})
    if libro is None:
        return None

    # Obtener autor_id como ObjectId
    autor_id = libro.get("autor_id")
    if autor_id and not isinstance(autor_id, ObjectId):
        autor_id = ObjectId(autor_id)

    # Buscar autor
    autor = db.autores.find_one({"_id": autor_id}) if autor_id else None

    # Buscar imágenes del libro actual
    imagenes = list(db.imagenes.find({"libro_id": ObjectId(id)}))

    # Agregar URL a las imágenes
    for img in imagenes:
        if img.get("path_local"):
            filename = os.path.basename(img["path_local"])
            img["url"] = f"/static/imagenes/{filename}"

        img.pop("embedding_visual", None)
        img.pop("modelo_vision", None)

    imagenes = parse_mongo_document(imagenes)

    # Buscar libros relacionados (mismo autor, excepto el actual)
    relacionados = list(
        db.libros.find({
            "autor_id": autor_id,
            "_id": {"$ne": ObjectId(id)}
        }).limit(5)
    ) if autor_id else []

    # Agregar imagen a cada libro relacionado
    for libro_rel in relacionados:
        imagen = db.imagenes.find_one({
            "libro_id": libro_rel["_id"],
            "tipo": "portada"
        })

        if imagen and imagen.get("path_local"):
            filename = os.path.basename(imagen["path_local"])
            libro_rel["imagen"] = (
                f"http://localhost:8000/static/imagenes/{filename}"
            )
        else:
            libro_rel["imagen"] = None

    relacionados = parse_mongo_document(relacionados)

    # Convertir libro y autor
    libro = parse_mongo_document(libro)
    autor = parse_mongo_document(autor)

    # Agregar imagen principal al libro
    if imagenes:
        libro["imagen"] = f"http://localhost:8000{imagenes[0]['url']}"
    else:
        libro["imagen"] = None
        
    
    return {
        "book": libro,
        "author": autor,
        "images": imagenes,
        "related": relacionados
    }


def insertar_libro(data):
    resultado = db.libros.insert_one(data)
    return str(resultado.inserted_id)


def actualizar_libro(id, data):
    db.libros.update_one({"_id": ObjectId(id)}, {"$set": data})
    return True


def eliminar_libro(id):
    db.libros.delete_one({"_id": ObjectId(id)})
    return True