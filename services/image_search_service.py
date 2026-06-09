from config.database import get_database
from services.image_embedding_service import get_image_embedding
from repositories.libros_repository import get_complete_book
import numpy as np


db = get_database()

def search_similar_books(
    image_path: str,
    top_k: int = 5
):
    
    resultados = search_similar_images(
        image_path=image_path,
        top_k=top_k
    )

    libros_vistos = set()
    libros = []

    for resultado in resultados:

        libro_id = resultado["libro_id"]

        if libro_id in libros_vistos:
            continue

        libros_vistos.add(libro_id)

        libro = get_complete_book(libro_id)

        libros.append({
            "score": resultado["score"],
            "book_data": libro
        })

    return libros

def cosine_similarity(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)

    return np.dot(v1, v2) / (
        np.linalg.norm(v1) * np.linalg.norm(v2)
    )


def search_similar_images(
    image_path: str,
    top_k: int = 5
):

    query_embedding = get_image_embedding(image_path)

    imagenes = list(
        db.imagenes.find(
            {
                "embedding_visual": {
                    "$exists": True
                }
            }
        )
    )

    resultados = []

    for imagen in imagenes:

        score = cosine_similarity(
            query_embedding,
            imagen["embedding_visual"]
        )

        resultados.append({
            "imagen_id": str(imagen["_id"]),
            "libro_id": str(imagen["libro_id"]),
            "path_local": imagen["path_local"],
            "score": float(score)
        })

    resultados.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return resultados[:top_k]