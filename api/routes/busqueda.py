from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from services.retrieval_service import search_chunks, search_books_text

from fastapi.responses import JSONResponse
from utils.mongo_helpers import serialize_doc

router = APIRouter(tags=["Búsqueda"])

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)
    top_k: int = Field(default=5, ge=1, le=20)

@router.post("/search")
def buscar(request: SearchRequest):
    try:
        chunks = search_chunks(query=request.query, top_k=request.top_k)
        books = search_books_text(query=request.query, limit=5)
        return JSONResponse(content=serialize_doc({
            "query": request.query,
            "chunks": chunks,
            "books": books,
            "total_chunks": len(chunks),
            "total_books": len(books)
        }))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))