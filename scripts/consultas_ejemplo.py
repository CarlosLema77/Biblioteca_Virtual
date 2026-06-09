"""
consultas_ejemplo.py
5 consultas de ejemplo documentadas para el informe del proyecto.
Ejecutar con la API corriendo: uvicorn main:app --reload

Cada consulta muestra el request, la respuesta esperada y su caso de uso.
Puedes correr este archivo directamente o copiar los curl como evidencia.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def separador(titulo: str):
    print("\n" + "="*60)
    print(f"  {titulo}")
    print("="*60)


# ─────────────────────────────────────────────────────────────
# CONSULTA 1 — Búsqueda semántica general
# Caso de uso: RF-01 — El usuario busca libros por tema general
# ─────────────────────────────────────────────────────────────
separador("CONSULTA 1 · Búsqueda semántica general")

request_1 = {
    "query": "inteligencia artificial aprendizaje automático",
    "top_k": 5,
    "idioma": "es"
}

print("REQUEST  POST /search")
print(json.dumps(request_1, ensure_ascii=False, indent=2))

resp = requests.post(f"{BASE_URL}/search", json=request_1)
print("\nRESPONSE")
print(json.dumps(resp.json(), ensure_ascii=False, indent=2))

# curl equivalente:
# curl -X POST http://localhost:8000/search \
#   -H "Content-Type: application/json" \
#   -d '{"query": "inteligencia artificial aprendizaje automático", "top_k": 5, "idioma": "es"}'


# ─────────────────────────────────────────────────────────────
# CONSULTA 2 — Pregunta técnica al RAG
# Caso de uso: RF-05 — El usuario hace una pregunta en lenguaje natural
# ─────────────────────────────────────────────────────────────
separador("CONSULTA 2 · Pregunta técnica al pipeline RAG")

request_2 = {
    "question": "¿Qué es el aprendizaje profundo y cómo se diferencia del machine learning tradicional?",
    "top_k": 5,
    "idioma": "es"
}

print("REQUEST  POST /rag")
print(json.dumps(request_2, ensure_ascii=False, indent=2))

resp = requests.post(f"{BASE_URL}/rag", json=request_2)
data = resp.json()
print("\nRESPONSE")
print(f"Pregunta:     {data['question']}")
print(f"Chunks usados: {data['num_chunks']}")
print(f"Modelo LLM:   {data['model']}")
print(f"Tokens totales: {data['tokens_used']['total_tokens']}")
print(f"\nRespuesta del LLM:\n{data['answer']}")


# ─────────────────────────────────────────────────────────────
# CONSULTA 3 — Búsqueda de concepto específico
# Caso de uso: RF-01 — Búsqueda por concepto técnico específico
# ─────────────────────────────────────────────────────────────
separador("CONSULTA 3 · Concepto técnico específico")

request_3 = {
    "question": "Explica el concepto de embeddings y para qué se usan en NLP",
    "top_k": 4
}

print("REQUEST  POST /rag")
print(json.dumps(request_3, ensure_ascii=False, indent=2))

resp = requests.post(f"{BASE_URL}/rag", json=request_3)
data = resp.json()
print(f"\nRespuesta:\n{data['answer']}")
print(f"\nChunks recuperados:")
for i, chunk in enumerate(data['chunks_used'], 1):
    print(f"  {i}. Score: {chunk['score']:.4f} | Estrategia: {chunk['estrategia_chunking']}")
    print(f"     Texto: {chunk['chunk_texto'][:100]}...")


# ─────────────────────────────────────────────────────────────
# CONSULTA 4 — Pregunta comparativa
# Caso de uso: RF-05 — Consulta que requiere comparar información
# de múltiples fragmentos (prueba el razonamiento del LLM)
# ─────────────────────────────────────────────────────────────
separador("CONSULTA 4 · Pregunta comparativa entre conceptos")

request_4 = {
    "question": "¿Cuáles son las diferencias entre Word2Vec, GloVe y BERT para representar texto?",
    "top_k": 5,
    "idioma": "es"
}

print("REQUEST  POST /rag")
print(json.dumps(request_4, ensure_ascii=False, indent=2))

resp = requests.post(f"{BASE_URL}/rag", json=request_4)
data = resp.json()
print(f"\nRespuesta:\n{data['answer']}")


# ─────────────────────────────────────────────────────────────
# CONSULTA 5 — Pregunta fuera del contexto (prueba de robustez)
# Caso de uso: Verificar que el sistema NO alucina cuando no tiene
# información suficiente — comportamiento esperado: el LLM debe
# responder que no encontró información sobre ese tema.
# ─────────────────────────────────────────────────────────────
separador("CONSULTA 5 · Tema fuera del contexto (prueba de robustez RAG)")

request_5 = {
    "question": "¿Cuáles son las recetas de cocina más populares de Colombia?",
    "top_k": 5
}

print("REQUEST  POST /rag")
print(json.dumps(request_5, ensure_ascii=False, indent=2))

resp = requests.post(f"{BASE_URL}/rag", json=request_5)
data = resp.json()
print(f"\nRespuesta esperada: El LLM indica que no hay información disponible.")
print(f"\nRespuesta real del LLM:\n{data['answer']}")

# Esta consulta valida que el prompt engineering funciona correctamente:
# el LLM NO debe inventar recetas de cocina aunque las conozca,
# debe limitarse al contexto de la biblioteca.


print("\n" + "="*60)
print("  FIN DE LAS 5 CONSULTAS DE EJEMPLO")
print("="*60)