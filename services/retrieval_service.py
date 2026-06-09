"""
retrieval_service.py
Busca los chunks más relevantes en MongoDB usando Vector Search.
Retorna los top-K chunks semánticamente similares a la consulta.
"""

from pymongo import MongoClient
from pymongo.collection import Collection
from services.embedding_service import get_embedding
import os
from dotenv import load_dotenv

load_dotenv()

_client = MongoClient(os.getenv("MONGODB_URI"))
_db = _client[os.getenv("DB_NAME")]


def search_chunks(query: str, top_k: int = 5, idioma: str = None) -> list[dict]:
    """
    Busca los top_k chunks más relevantes para la consulta dada.
    
    Args:
        query:  Pregunta o texto de búsqueda del usuario.
        top_k:  Cantidad de chunks a recuperar (default 5).
        idioma: Filtro opcional por idioma (ej: "es", "en").
    
    Returns:
        Lista de dicts con chunk_texto, doc_id, score y estrategia_chunking.
    """
    query_vector = get_embedding(query)

    # Pipeline de búsqueda híbrida:
    # 1. $vectorSearch: encuentra los candidatos semánticamente similares
    # 2. $match: filtra por idioma si se especificó
    # 3. $project: selecciona solo los campos necesarios + score

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",       # Nombre del índice Atlas Vector Search
                "queryVector": query_vector,
                "path": "embedding",
                "numCandidates": top_k * 10,   # Examina 10x más candidatos para mayor calidad
                "limit": top_k
            }
        },
        {
            "$project": {
                "_id": 1,
                "chunk_texto": 1,
                "doc_id": 1,
                "estrategia_chunking": 1,
                "idioma": 1,
                "num_tokens": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]

    # Insertar filtro de idioma después del vectorSearch si se especificó
    if idioma:
        pipeline.insert(1, {"$match": {"idioma": idioma}})

    chunks = list(_db["chunks"].aggregate(pipeline))

    # Convertir ObjectId a string para poder serializar a JSON
    for chunk in chunks:
        chunk["_id"] = str(chunk["_id"])
        chunk["doc_id"] = str(chunk["doc_id"])

    return chunks


def search_books_text(query: str, limit: int = 10) -> list[dict]:
    """
    Búsqueda por texto completo en título y descripción de libros.
    Usa el índice de texto creado en la colección libros.
    Complementa la búsqueda vectorial con resultados keyword-based.
    
    Args:
        query: Palabras clave a buscar.
        limit: Máximo de resultados a retornar.
    
    Returns:
        Lista de libros con título, tipo, idioma y score de relevancia.
    """
    cursor = _db["libros"].find(
        {"$text": {"$search": query}},
        {
            "titulo": 1,
            "tipo": 1,
            "idioma": 1,
            "descripcion": 1,
            "score": {"$meta": "textScore"}
        }
    ).sort([("score", {"$meta": "textScore"})]).limit(limit)

    results = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        results.append(doc)

    return results