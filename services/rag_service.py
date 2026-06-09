"""
rag_service.py
Pipeline RAG completo:
  1. Recupera los chunks más relevantes (retrieval)
  2. Construye el prompt con contexto + pregunta (prompt engineering)
  3. Llama a Groq API con Llama 3.1 para generar la respuesta (generation)
"""

from groq import Groq
from services.retrieval_service import search_chunks
import os
from dotenv import load_dotenv

load_dotenv()

_groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Modelo a usar — Llama 3.1 8B es el más rápido en Groq Free Tier
GROQ_MODEL = "llama-3.1-8b-instant"


def _build_prompt(question: str, chunks: list[dict]) -> str:
    """
    Construye el prompt para el LLM usando los chunks recuperados como contexto.
    
    Estrategia de prompt engineering:
    - System prompt: define el rol del asistente y las reglas de respuesta
    - User prompt: contexto de los chunks + pregunta del usuario
    - Se instruye al modelo a responder SOLO con lo que está en el contexto
      para evitar alucinaciones (hallucinations)
    """
    # Construir el bloque de contexto concatenando los chunks recuperados
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        score = chunk.get("score", 0)
        estrategia = chunk.get("estrategia_chunking", "desconocida")
        context_parts.append(
            f"[Fragmento {i} | Relevancia: {score:.3f} | Estrategia: {estrategia}]\n"
            f"{chunk['chunk_texto']}"
        )
    
    context = "\n\n---\n\n".join(context_parts)
    
    if not context.strip():
        context = "No se encontraron fragmentos relevantes en la base de datos."

    prompt = f"""Eres un asistente experto de la Biblioteca Virtual. Tu tarea es responder preguntas usando EXCLUSIVAMENTE la información de los fragmentos de texto proporcionados a continuación.

REGLAS IMPORTANTES:
- Responde SOLO con información presente en los fragmentos.
- Si la información no está en los fragmentos, di claramente: "No encontré información suficiente sobre esto en la biblioteca."
- Sé preciso, claro y conciso. Máximo 3 párrafos.
- Si hay contradicciones entre fragmentos, menciónalas.
- Responde en el mismo idioma en que está escrita la pregunta.

=== FRAGMENTOS RECUPERADOS ===
{context}
=== FIN DE FRAGMENTOS ===

PREGUNTA: {question}

RESPUESTA:"""

    return prompt


def run_rag_pipeline(question: str, top_k: int = 5, idioma: str = None) -> dict:
    """
    Ejecuta el pipeline RAG completo y retorna la respuesta con metadatos.
    
    Args:
        question: Pregunta en lenguaje natural del usuario.
        top_k:    Número de chunks a recuperar como contexto.
        idioma:   Filtro de idioma opcional para la recuperación.
    
    Returns:
        Dict con:
          - answer:   Respuesta generada por el LLM
          - chunks:   Chunks usados como contexto
          - model:    Modelo LLM utilizado
          - question: Pregunta original
    """
    # --- PASO 1: RETRIEVAL ---
    # Recuperar los chunks más relevantes semánticamente
    chunks = search_chunks(query=question, top_k=top_k, idioma=idioma)

    # --- PASO 2: PROMPT ENGINEERING ---
    # Construir el prompt con los chunks como contexto
    prompt = _build_prompt(question=question, chunks=chunks)

    # --- PASO 3: GENERATION ---
    # Llamar a Groq API con Llama 3.1 para generar la respuesta
    completion = _groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente de biblioteca académica. "
                    "Respondes preguntas sobre libros, artículos y textos académicos "
                    "usando únicamente el contexto proporcionado. "
                    "Eres preciso, claro y siempre indicas cuando no tienes suficiente información."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,      # Baja temperatura = respuestas más precisas y deterministas
        max_tokens=1024,      # Máximo de tokens en la respuesta
        top_p=0.9
    )

    answer = completion.choices[0].message.content

    return {
        "question": question,
        "answer": answer,
        "chunks_used": chunks,
        "num_chunks": len(chunks),
        "model": GROQ_MODEL,
        "tokens_used": {
            "prompt_tokens": completion.usage.prompt_tokens,
            "completion_tokens": completion.usage.completion_tokens,
            "total_tokens": completion.usage.total_tokens
        }
    }