"""
S: Solo se encarga de ejecutar el experimento de chunking
D: Depende de get_database() como abstracción
"""
import os
from datetime import datetime, timezone
from sentence_transformers import SentenceTransformer
from config.database import get_database

MODELO = "all-MiniLM-L6-v2"

CONSULTAS = [
    {"id": 1,  "texto": "What books talk about artificial intelligence?",          "tipo": "Semántica general"},
    {"id": 2,  "texto": "What are the main themes of the book?",                   "tipo": "Resumen temático"},
    {"id": 3,  "texto": "What does the author say about climate change?",          "tipo": "Búsqueda específica"},
    {"id": 4,  "texto": "Explain the concept of entropy according to documents",   "tipo": "Concepto técnico"},
    {"id": 5,  "texto": "What characters appear in fantasy novels?",               "tipo": "Narrativo"},
    {"id": 6,  "texto": "What are the conclusions of the article about economy?",  "tipo": "Estructura académica"},
    {"id": 7,  "texto": "What similarities exist between suspense books?",         "tipo": "Comparativo"},
    {"id": 8,  "texto": "Describe the atmosphere in horror novels",                "tipo": "Descriptivo narrativo"},
    {"id": 9,  "texto": "What recommendations does the author give for learning?", "tipo": "Extracción de consejos"},
    {"id": 10, "texto": "Differences between science fiction and fantasy",         "tipo": "Análisis comparativo"},
]

ESTRATEGIAS = ["fixed-size", "sentence-aware", "semantic"]


def buscar_chunks(db, embedding: list, estrategia: str, top_k: int = 3) -> list:
    """
    S: Solo ejecuta una búsqueda vectorial para una estrategia
    """
    pipeline = [
        {
            "$vectorSearch": {
                "index":         "vector_index_chunks",
                "path":          "embedding",
                "queryVector":   embedding,
                "numCandidates": 50,
                "limit":         top_k,
                "filter":        {"estrategia_chunking": {"$eq": estrategia}}
            }
        },
        {
            "$project": {
                "chunk_texto":         1,
                "estrategia_chunking": 1,
                "num_tokens":          1,
                "score": {"$meta":     "vectorSearchScore"}
            }
        }
    ]
    return list(db["chunks"].aggregate(pipeline))


def ejecutar_experimento():
    print("🚀 Iniciando experimento de chunking...\n")

    db     = get_database()
    modelo = SentenceTransformer(MODELO)

    resultados = []

    for consulta in CONSULTAS:
        print(f"🔍 Consulta {consulta['id']}: {consulta['texto']}")

        # Generar embedding de la consulta
        embedding = modelo.encode(consulta["texto"]).tolist()

        resultado_consulta = {
            "consulta_id":   consulta["id"],
            "consulta_texto": consulta["texto"],
            "tipo":          consulta["tipo"],
            "estrategias":   {}
        }

        for estrategia in ESTRATEGIAS:
            chunks = buscar_chunks(db, embedding, estrategia)

            resultado_consulta["estrategias"][estrategia] = {
                "chunks_recuperados": len(chunks),
                "chunks": [
                    {
                        "texto":      c["chunk_texto"][:200],  # primeros 200 chars
                        "score":      round(c.get("score", 0), 4),
                        "num_tokens": c.get("num_tokens", 0)
                    }
                    for c in chunks
                ]
            }
            print(f"  ✅ {estrategia}: {len(chunks)} chunks recuperados")

        resultados.append(resultado_consulta)
        print()

    # Guardar resultados en MongoDB
    coleccion = db["evaluaciones"] if "evaluaciones" in db.list_collection_names() else db.create_collection("evaluaciones")
    db["evaluaciones"].insert_one({
        "fecha":      datetime.now(timezone.utc),
        "modelo":     MODELO,
        "resultados": resultados
    })

    # Mostrar resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DEL EXPERIMENTO")
    print("="*60)

    for r in resultados:
        print(f"\nConsulta {r['consulta_id']} — {r['tipo']}")
        print(f"  '{r['consulta_texto'][:50]}...'")
        for est, data in r["estrategias"].items():
            if data["chunks"]:
                mejor_score = data["chunks"][0]["score"]
                print(f"  {est:20} → score: {mejor_score:.4f}")

    print("\n🎉 Experimento completado y guardado en MongoDB!")


if __name__ == "__main__":
    ejecutar_experimento()