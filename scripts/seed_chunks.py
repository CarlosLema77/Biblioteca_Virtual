"""
seed_chunks.py
Inserta chunks de prueba en MongoDB con sus embeddings generados.
Ejecutar UNA SOLA VEZ antes de probar los endpoints:
  python scripts/seed_chunks.py

Inserta 10 chunks reales con embeddings de las 3 estrategias,
asociados a libros ficticios del dominio de la biblioteca.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from services.embedding_service import get_embedding
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("DB_NAME")]

# IDs ficticios de libros para asociar los chunks
LIBRO_IA_ID    = ObjectId()
LIBRO_ML_ID    = ObjectId()
LIBRO_NLP_ID   = ObjectId()

# Textos representativos del dominio de la biblioteca
CHUNKS_DATA = [
    {
        "doc_id": LIBRO_IA_ID,
        "chunk_index": 0,
        "estrategia_chunking": "sentence-aware",
        "chunk_texto": (
            "La inteligencia artificial es una rama de la informática que busca crear "
            "sistemas capaces de realizar tareas que normalmente requieren inteligencia humana. "
            "Entre sus aplicaciones más destacadas se encuentran el reconocimiento de voz, "
            "la visión por computadora y el procesamiento del lenguaje natural."
        ),
        "modelo": "all-MiniLM-L6-v2",
        "num_tokens": 62,
        "idioma": "es",
        "fecha_ingesta": datetime.utcnow()
    },
    {
        "doc_id": LIBRO_IA_ID,
        "chunk_index": 1,
        "estrategia_chunking": "sentence-aware",
        "chunk_texto": (
            "El aprendizaje automático, o machine learning, es un subcampo de la inteligencia "
            "artificial que permite a los sistemas aprender y mejorar automáticamente a partir "
            "de la experiencia sin ser programados explícitamente. "
            "Los algoritmos de aprendizaje automático construyen modelos matemáticos basados en datos de entrenamiento."
        ),
        "modelo": "all-MiniLM-L6-v2",
        "num_tokens": 68,
        "idioma": "es",
        "fecha_ingesta": datetime.utcnow()
    },
    {
        "doc_id": LIBRO_ML_ID,
        "chunk_index": 0,
        "estrategia_chunking": "fixed-size",
        "chunk_texto": (
            "Las redes neuronales artificiales son sistemas de computación vagamente inspirados "
            "en las redes neuronales biológicas que constituyen los cerebros de los animales. "
            "El aprendizaje profundo o deep learning utiliza redes neuronales con múltiples capas "
            "para aprender representaciones de datos con múltiples niveles de abstracción."
        ),
        "modelo": "all-MiniLM-L6-v2",
        "num_tokens": 71,
        "idioma": "es",
        "fecha_ingesta": datetime.utcnow()
    },
    {
        "doc_id": LIBRO_ML_ID,
        "chunk_index": 1,
        "estrategia_chunking": "fixed-size",
        "chunk_texto": (
            "Los algoritmos de clasificación en machine learning incluyen regresión logística, "
            "árboles de decisión, máquinas de vectores de soporte y redes neuronales. "
            "La selección del algoritmo adecuado depende del tamaño del dataset, "
            "la naturaleza de los datos y el tipo de problema a resolver."
        ),
        "modelo": "all-MiniLM-L6-v2",
        "num_tokens": 65,
        "idioma": "es",
        "fecha_ingesta": datetime.utcnow()
    },
    {
        "doc_id": LIBRO_ML_ID,
        "chunk_index": 2,
        "estrategia_chunking": "fixed-size",
        "chunk_texto": (
            "El sobreajuste o overfitting ocurre cuando un modelo aprende demasiado bien "
            "los datos de entrenamiento, incluyendo su ruido, y no generaliza correctamente "
            "a nuevos datos. Para evitarlo se utilizan técnicas como la regularización L1 y L2, "
            "el dropout en redes neuronales y la validación cruzada."
        ),
        "modelo": "all-MiniLM-L6-v2",
        "num_tokens": 67,
        "idioma": "es",
        "fecha_ingesta": datetime.utcnow()
    },
    {
        "doc_id": LIBRO_NLP_ID,
        "chunk_index": 0,
        "estrategia_chunking": "semantic",
        "chunk_texto": (
            "El procesamiento del lenguaje natural (NLP) es un campo de la inteligencia artificial "
            "que se ocupa de la interacción entre computadoras y el lenguaje humano. "
            "Los transformers, introducidos en el paper 'Attention is All You Need' de 2017, "
            "revolucionaron el campo al permitir el procesamiento paralelo de secuencias de texto."
        ),
        "modelo": "all-MiniLM-L6-v2",
        "num_tokens": 73,
        "idioma": "es",
        "fecha_ingesta": datetime.utcnow()
    },
    {
        "doc_id": LIBRO_NLP_ID,
        "chunk_index": 1,
        "estrategia_chunking": "semantic",
        "chunk_texto": (
            "Los embeddings de palabras como Word2Vec y GloVe representan palabras como vectores "
            "densos en un espacio de alta dimensión, donde palabras semánticamente similares "
            "tienen representaciones vectoriales cercanas. "
            "BERT y sus variantes generan embeddings contextuales que capturan el significado "
            "de una palabra según su contexto en la oración."
        ),
        "modelo": "all-MiniLM-L6-v2",
        "num_tokens": 75,
        "idioma": "es",
        "fecha_ingesta": datetime.utcnow()
    },
    {
        "doc_id": LIBRO_NLP_ID,
        "chunk_index": 2,
        "estrategia_chunking": "semantic",
        "chunk_texto": (
            "Los sistemas de recuperación de información aumentada por generación, conocidos como RAG, "
            "combinan la búsqueda semántica con modelos de lenguaje grande para responder preguntas. "
            "El proceso consiste en vectorizar la consulta, recuperar fragmentos relevantes de una base "
            "de datos vectorial y usar esos fragmentos como contexto para que el LLM genere la respuesta."
        ),
        "modelo": "all-MiniLM-L6-v2",
        "num_tokens": 78,
        "idioma": "es",
        "fecha_ingesta": datetime.utcnow()
    },
    {
        "doc_id": LIBRO_IA_ID,
        "chunk_index": 2,
        "estrategia_chunking": "sentence-aware",
        "chunk_texto": (
            "La ética en la inteligencia artificial aborda preguntas fundamentales sobre el impacto "
            "social de los sistemas automatizados. Los sesgos en los datos de entrenamiento pueden "
            "perpetuar discriminaciones existentes. Es fundamental diseñar sistemas de IA que sean "
            "transparentes, justos y explicables para garantizar su uso responsable."
        ),
        "modelo": "all-MiniLM-L6-v2",
        "num_tokens": 69,
        "idioma": "es",
        "fecha_ingesta": datetime.utcnow()
    },
    {
        "doc_id": LIBRO_ML_ID,
        "chunk_index": 3,
        "estrategia_chunking": "fixed-size",
        "chunk_texto": (
            "El cambio climático es uno de los mayores desafíos que enfrenta la humanidad en el siglo XXI. "
            "Los modelos de inteligencia artificial están siendo utilizados para predecir patrones climáticos, "
            "optimizar el consumo energético y acelerar el desarrollo de energías renovables. "
            "El aprendizaje automático permite analizar grandes volúmenes de datos meteorológicos."
        ),
        "modelo": "all-MiniLM-L6-v2",
        "num_tokens": 72,
        "idioma": "es",
        "fecha_ingesta": datetime.utcnow()
    }
]


def seed():
    collection = db["chunks"]
    
    # Limpiar chunks anteriores de prueba para evitar duplicados
    collection.delete_many({"modelo": "all-MiniLM-L6-v2", "idioma": "es"})
    print("Chunks anteriores eliminados.")

    print("Generando embeddings y insertando chunks...")
    for i, chunk in enumerate(CHUNKS_DATA):
        # Generar embedding del texto
        chunk["embedding"] = get_embedding(chunk["chunk_texto"])
        print(f"  [{i+1}/{len(CHUNKS_DATA)}] Chunk {chunk['chunk_index']} "
              f"({chunk['estrategia_chunking']}) — {chunk['num_tokens']} tokens")

    # Insertar todos de una vez
    result = collection.insert_many(CHUNKS_DATA)
    print(f"\n✓ {len(result.inserted_ids)} chunks insertados correctamente.")
    print("Ya puedes probar los endpoints /search y /rag.")


if __name__ == "__main__":
    seed()