from config.database import get_database
from bson import ObjectId
from utils.mongo_helpers import parse_mongo_document



db = get_database()


def get_all_authors():

    autores = list(db.autores.find())

    return parse_mongo_document(autores)


def get_author(id):
    autor = db.autores.find_one({"_id": ObjectId(id)})
    libros = list(db.libros.find({"autor_id": ObjectId(id)}))
    return {
        "author": parse_mongo_document(autor),
        "books": parse_mongo_document(libros)
    }
    


def get_complete_author(id):
    autor = db.autores.find_one({"_id": ObjectId(id)})
    libros = list(db.libros.find({"autor_id": ObjectId(id)}))
    return {
        "author": parse_mongo_document(autor),
        "books": parse_mongo_document(libros)
    }