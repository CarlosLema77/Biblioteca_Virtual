"""
embedding_service.py
Genera embeddings de texto usando all-MiniLM-L6-v2 (384 dimensiones).
Se instancia una sola vez al arrancar la app (patrón singleton liviano).
"""

from sentence_transformers import SentenceTransformer

# Carga el modelo una sola vez en memoria al importar el módulo.
# La primera vez descarga el modelo (~90 MB), las siguientes es instantáneo.
_model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str) -> list[float]:
    """
    Recibe un string y devuelve su embedding como lista de 384 floats.
    Normaliza el texto antes de procesar (strip de espacios).
    """
    text = text.strip()
    if not text:
        raise ValueError("El texto para generar embedding no puede estar vacío.")
    
    embedding = _model.encode(text, normalize_embeddings=True)
    return embedding.tolist()