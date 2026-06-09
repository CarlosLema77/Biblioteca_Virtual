from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from services.retrieval_service import search_chunks, search_books_text
from services.rag_service import run_rag_pipeline
from api.main import router as api_router
from pydantic import BaseModel, Field

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/test")
def test():
    return {"message": "Server is working"}

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)
    top_k: int = Field(default=5, ge=1, le=20)
    idioma: str | None = None

class RAGRequest(BaseModel):
    question: str = Field(..., min_length=10, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=10)
    idioma: str | None = None

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/search")
def search(request: SearchRequest):
    try:
        chunks = search_chunks(query=request.query, top_k=request.top_k, idioma=request.idioma)
        books = search_books_text(query=request.query, limit=5)
        return {"query": request.query, "chunks": chunks, "books": books}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/rag")
def rag(request: RAGRequest):
    try:
        result = run_rag_pipeline(question=request.question, top_k=request.top_k, idioma=request.idioma)
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

app.include_router(api_router)