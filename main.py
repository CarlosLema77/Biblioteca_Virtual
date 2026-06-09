"""
main.py
API REST de la Biblioteca Virtual.
Endpoints:
  POST /search  → Búsqueda semántica de chunks + texto completo en libros
  POST /rag     → Pipeline RAG completo: recuperación + generación con LLM
  GET  /health  → Health check del servidor
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from services.retrieval_service import search_chunks, search_books_text
from services.rag_service import run_rag_pipeline

# ── Instancia de la app ──────────────────────────────────────────────────────
app = FastAPI(
    title="Biblioteca Virtual API",
    description=(
        "API REST del sistema RAG de la Biblioteca Virtual. "
        "Permite búsqueda semántica sobre el catálogo de libros y consultas "
        "en lenguaje natural respondidas por un LLM (Llama 3.1 vía Groq)."
    ),
    version="1.0.0"
)


# ── Schemas de Request y Response ────────────────────────────────────────────

class SearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Texto o palabras clave para buscar en la biblioteca.",
        example="inteligencia artificial aprendizaje automático"
    )
    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Número de chunks a recuperar (entre 1 y 20)."
    )
    idioma: str | None = Field(
        default=None,
        description="Filtro de idioma ISO 639-1 (ej: 'es', 'en'). Opcional."
    )


class RAGRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="Pregunta en lenguaje natural para el sistema RAG.",
        example="¿Qué técnicas de aprendizaje profundo se mencionan en los libros?"
    )
    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Número de chunks a usar como contexto para el LLM."
    )
    idioma: str | None = Field(
        default=None,
        description="Filtrar chunks por idioma antes de pasarlos al LLM. Opcional."
    )


# ── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/health", tags=["Sistema"])
def health_check():
    """
    Verifica que la API está corriendo correctamente.
    Útil para monitoreo y para confirmar que los servicios arrancan bien.
    """
    return {
        "status": "ok",
        "service": "Biblioteca Virtual API",
        "version": "1.0.0"
    }


@app.post("/search", tags=["Búsqueda"])
def search(request: SearchRequest):
    """
    **Búsqueda semántica** sobre los chunks vectorizados de la biblioteca.
    
    Combina dos tipos de búsqueda:
    - **Vectorial**: encuentra chunks semánticamente similares a la consulta
      usando los embeddings almacenados en MongoDB Atlas Vector Search.
    - **Texto completo**: encuentra libros que contienen las palabras clave
      usando el índice de texto de la colección `libros`.
    
    Retorna los chunks más relevantes y los libros relacionados.
    """
    try:
        # Búsqueda vectorial en chunks
        chunks = search_chunks(
            query=request.query,
            top_k=request.top_k,
            idioma=request.idioma
        )

        # Búsqueda por texto en libros
        books = search_books_text(query=request.query, limit=5)

        return {
            "query": request.query,
            "chunks": chunks,
            "books": books,
            "total_chunks": len(chunks),
            "total_books": len(books)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la búsqueda: {str(e)}"
        )


@app.post("/rag", tags=["RAG"])
def rag(request: RAGRequest):
    """
    **Pipeline RAG completo** — Recuperación + Generación con LLM.
    
    Proceso interno:
    1. Genera el embedding de la pregunta con `all-MiniLM-L6-v2`.
    2. Recupera los `top_k` chunks más relevantes de MongoDB mediante Vector Search.
    3. Construye un prompt con los chunks como contexto.
    4. Llama a Groq API (Llama 3.1) para generar la respuesta.
    5. Retorna la respuesta junto con los chunks usados y métricas de tokens.
    
    La respuesta del LLM se basa **exclusivamente** en el contenido de los
    chunks recuperados, evitando alucinaciones sobre información no disponible.
    """
    try:
        result = run_rag_pipeline(
            question=request.question,
            top_k=request.top_k,
            idioma=request.idioma
        )
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en el pipeline RAG: {str(e)}"
        )