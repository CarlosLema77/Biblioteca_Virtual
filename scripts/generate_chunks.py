"""
S: Solo se encarga de generar chunks con embeddings y guardarlos en MongoDB
D: Depende de get_database() y ChunkingStrategy como abstracciones
O: Para agregar una nueva estrategia solo se agrega al diccionario ESTRATEGIAS
"""
from datetime import datetime, timezone
from sentence_transformers import SentenceTransformer
from config.database import get_database
from chunking.strategies import FixedSizeChunking, SentenceAwareChunking, SemanticChunking
import os


# O: Agregar nueva estrategia = solo agregar una línea aquí
ESTRATEGIAS = {
    "fixed-size":     FixedSizeChunking(chunk_size=256, overlap=32),
    "sentence-aware": SentenceAwareChunking(max_oraciones=5, overlap_oraciones=1),
    "semantic":       SemanticChunking(umbral_similitud=0.80),
}

MODELO_EMBEDDINGS = "all-MiniLM-L6-v2"


def get_modelo_embeddings() -> SentenceTransformer:
    """D: Abstracción para obtener el modelo de embeddings"""
    print(f"🤖 Cargando modelo {MODELO_EMBEDDINGS}...")
    return SentenceTransformer(MODELO_EMBEDDINGS)


def procesar_libro(db, libro: dict, modelo: SentenceTransformer):
    """
    S: Solo procesa un libro — genera chunks con las 3 estrategias
       y los guarda en MongoDB
    """
    coleccion_chunks = db["chunks"]
    coleccion_libros = db["libros"]
    titulo           = libro["titulo"]
    # Leer texto desde archivo local en lugar de MongoDB
    # Construir nombre de archivo desde el campo guardado
    # Si no existe en MongoDB, buscarlo en el JSON local
    nombre_archivo = libro.get("nombre_archivo", "")
    
    if not nombre_archivo:
        # Buscar en el JSON de libros
        import json
        with open(os.path.join("data", "libros.json"), "r", encoding="utf-8") as f:
            libros_json = json.load(f)
        match = next((l for l in libros_json if l["titulo"] == libro["titulo"]), None)
        if match:
            nombre_archivo = match["nombre_archivo"]
        else:
            print(f"  ⚠️  No se encontró nombre_archivo para: {libro['titulo']}")
            return

    path_txt = os.path.join("data", "textos", nombre_archivo)
    
    if not os.path.exists(path_txt):
        print(f"  ⚠️  Archivo no encontrado: {path_txt}")
        return

    with open(path_txt, "r", encoding="utf-8", errors="ignore") as f:
        texto = f.read()[:50000]  # Solo primeros 50,000 caracteres

    if not texto:
        print(f"  ⚠️  Sin texto: {titulo}")
        return

    chunks_ids_libro = []

    for nombre_estrategia, estrategia in ESTRATEGIAS.items():
        # Verificar si ya existen chunks para este libro y estrategia
        existentes = coleccion_chunks.count_documents({
            "doc_id":              libro["_id"],
            "estrategia_chunking": nombre_estrategia
        })
        if existentes > 0:
            print(f"  ⚠️  Ya existen chunks ({nombre_estrategia}): {titulo}")
            continue

        # Generar chunks
        chunks_texto = estrategia.split(texto)
        if not chunks_texto:
            print(f"  ⚠️  Sin chunks generados ({nombre_estrategia}): {titulo}")
            continue

        # Generar embeddings para todos los chunks de una vez (más eficiente)
        print(f"  🔄 Generando embeddings ({nombre_estrategia}): {len(chunks_texto)} chunks...")
        embeddings = modelo.encode(chunks_texto, show_progress_bar=False)

        # Guardar cada chunk en MongoDB
        docs = []
        for i, (chunk_texto, embedding) in enumerate(zip(chunks_texto, embeddings)):
            doc = {
                "doc_id":              libro["_id"],
                "chunk_index":         i,
                "estrategia_chunking": nombre_estrategia,
                "chunk_texto":         chunk_texto,
                "embedding":           embedding.tolist(),
                "modelo":              MODELO_EMBEDDINGS,
                "num_tokens":          len(chunk_texto.split()),
                "idioma":              libro.get("idioma", "en"),
                "fecha_ingesta":       datetime.now(timezone.utc)
            }
            docs.append(doc)

        # Insertar en lotes de 100 para no saturar la conexión
        BATCH_SIZE = 100
        ids_insertados = []
        for start in range(0, len(docs), BATCH_SIZE):
            batch = docs[start:start + BATCH_SIZE]
            result = coleccion_chunks.insert_many(batch)
            ids_insertados.extend(result.inserted_ids)

        chunks_ids_libro.extend(ids_insertados)
        print(f"  ✅ Guardados {len(docs)} chunks ({nombre_estrategia})")

    # Actualizar el libro con referencias a sus chunks
    if chunks_ids_libro:
        coleccion_libros.update_one(
            {"_id": libro["_id"]},
            {"$push": {"chunks_ids": {"$each": chunks_ids_libro}}}
        )


def generate_all_chunks():
    print("🚀 Iniciando generación de chunks y embeddings...\n")

    db     = get_database()
    modelo = get_modelo_embeddings()
    libros = list(db["libros"].find({}))

    print(f"\n📚 Procesando {len(libros)} libros con 3 estrategias...\n")

    for i, libro in enumerate(libros, 1):
        print(f"[{i}/{len(libros)}] {libro['titulo']}")
        procesar_libro(db, libro, modelo)
        print()

    total_chunks = db["chunks"].count_documents({})
    print(f"🎉 Generación completada!")
    print(f"   📦 Total chunks en MongoDB: {total_chunks}")
    print(f"   📊 Promedio por libro: {total_chunks // len(libros)}")


if __name__ == "__main__":
    generate_all_chunks()