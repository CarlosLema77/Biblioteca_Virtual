"""
seed_data.py
Puebla la base de datos con libros, autores, imágenes y chunks (con embeddings).
Ejecutar: python -m scripts.seed_data
"""

import json
import os
from datetime import datetime
from bson import ObjectId
from config.database import get_database
from services.embedding_service import get_embedding

# Conexión a la BD
db = get_database()

# Rutas de los datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIBROS_JSON = os.path.join(BASE_DIR, "data", "libros.json")
IMAGENES_JSON = os.path.join(BASE_DIR, "data", "imagenes.json")
TEXTOS_DIR = os.path.join(BASE_DIR, "data", "textos")

def chunk_text_simple(texto, tamano=500, solapamiento=50):
    """
    Función simple de chunking (fixed-size) en caso de que no tengas langchain o la estrategia propia.
    Divide el texto en fragmentos de aproximadamente `tamano` caracteres.
    """
    chunks = []
    inicio = 0
    while inicio < len(texto):
        fin = min(inicio + tamano, len(texto))
        # Retroceder hasta un punto de corte (espacio, punto, etc.) para no cortar palabras
        if fin < len(texto):
            while fin > inicio and texto[fin] not in (' ', '\n', '.', ',', ';', '?'):
                fin -= 1
        chunk = texto[inicio:fin].strip()
        if chunk:
            chunks.append(chunk)
        inicio = fin - solapamiento if fin - solapamiento > inicio else fin
    return chunks

def cargar_libros():
    with open(LIBROS_JSON, 'r', encoding='utf-8') as f:
        libros = json.load(f)
    return libros

def cargar_imagenes():
    with open(IMAGENES_JSON, 'r', encoding='utf-8') as f:
        imagenes = json.load(f)
    return imagenes

def leer_texto_libro(nombre_archivo):
    """
    Lee el contenido de un archivo de texto (de data/textos/)
    """
    ruta = os.path.join(TEXTOS_DIR, nombre_archivo)
    if not os.path.exists(ruta):
        print(f"Advertencia: no se encontró {ruta}")
        return ""
    with open(ruta, 'r', encoding='utf-8') as f:
        return f.read()

def insertar_autores(libros):
    """
    Extrae autores únicos de los libros y los inserta en la colección autores.
    Retorna un diccionario {nombre_autor: ObjectId}
    """
    autores_unicos = {}
    for libro in libros:
        autor_nombre = libro.get("autor")
        if autor_nombre and autor_nombre not in autores_unicos:
            # Verificar si ya existe en la BD
            existente = db.autores.find_one({"nombre": autor_nombre})
            if existente:
                autores_unicos[autor_nombre] = existente["_id"]
            else:
                nuevo_autor = {
                    "nombre": autor_nombre,
                    "nacionalidad": libro.get("nacionalidad", "Desconocida"),
                    "biografia": f"Biografía de {autor_nombre}",
                    "fecha_nacimiento": None,
                    "libros_ids": []
                }
                result = db.autores.insert_one(nuevo_autor)
                autores_unicos[autor_nombre] = result.inserted_id
    return autores_unicos

def insertar_libros_con_autores(libros, autores_ids):
    """
    Inserta los libros, vinculando el ObjectId del autor.
    Retorna un diccionario {titulo: libro_id}
    """
    libros_insertados = {}
    for libro in libros:
        autor_nombre = libro.get("autor")
        autor_id = autores_ids.get(autor_nombre)
        if not autor_id:
            print(f"Advertencia: no se encontró autor para {libro.get('titulo')}")
            continue
        nuevo_libro = {
            "titulo": libro["titulo"],
            "autor_id": autor_id,
            "genero": libro.get("genero", []),
            "idioma": libro.get("idioma", "es"),
            "tipo": libro.get("tipo", "novela"),
            "premium": libro.get("premium", False),
            "portada_id": None,
            "descripcion": libro.get("descripcion", ""),
            "resenias": [],
            "chunks_ids": []
        }
        result = db.libros.insert_one(nuevo_libro)
        libros_insertados[libro["titulo"]] = result.inserted_id
        # Actualizar el autor con el libro_id
        db.autores.update_one(
            {"_id": autor_id},
            {"$push": {"libros_ids": result.inserted_id}}
        )
    return libros_insertados

def insertar_imagenes(imagenes, libros_ids):
    """
    Inserta las imágenes, vinculando al libro correcto.
    Asume que en imagenes.json cada imagen tiene "libro_titulo" o "libro_id".
    """
    for img in imagenes:
        titulo_libro = img.get("libro_titulo")
        if not titulo_libro:
            continue
        libro_id = libros_ids.get(titulo_libro)
        if not libro_id:
            print(f"Advertencia: no se encontró libro para imagen {img.get('path_local')}")
            continue
        nueva_imagen = {
            "libro_id": libro_id,
            "tipo": img.get("tipo", "ilustracion"),
            "url": img.get("url"),
            "path_local": img.get("path_local"),
            "formato": img.get("formato"),
            "resolucion": img.get("resolucion"),
            "embedding_visual": None,
            "modelo_vision": None,
            "fecha_carga": datetime.now()
        }
        db.imagenes.insert_one(nueva_imagen)

def generar_chunks_y_embeddings(libros_ids, libros_originales):
    """
    Para cada libro, lee su archivo de texto (de data/textos/), genera chunks y embeddings,
    y los guarda en la colección `chunks`. Además actualiza el campo `chunks_ids` del libro.
    """
    # Diccionario para mapear título del libro -> nombre del archivo de texto
    # Asumimos que el nombre del archivo se puede inferir del título (por ejemplo, "Drácula" -> "dracula.txt")
    # O bien, en libros.json debe venir el campo "archivo_texto".
    for libro_original in libros_originales:
        titulo = libro_original["titulo"]
        libro_id = libros_ids.get(titulo)
        if not libro_id:
            continue
        # Obtener nombre del archivo de texto (puedes ajustarlo según tu convención)
        archivo_texto = libro_original.get("archivo_texto")
        if not archivo_texto:
            # Intento automático: normalizar título
            nombre_base = titulo.lower().replace(" ", "_").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
            archivo_texto = f"{nombre_base}.txt"
        texto_completo = leer_texto_libro(archivo_texto)
        if not texto_completo:
            print(f"No se encontró texto para {titulo} ({archivo_texto})")
            continue
        # Generar chunks (puedes usar la estrategia que prefieras)
        chunks_texto = chunk_text_simple(texto_completo, tamano=800, solapamiento=100)
        chunks_ids = []
        for idx, chunk in enumerate(chunks_texto):
            embedding = get_embedding(chunk)
            chunk_doc = {
                "doc_id": libro_id,
                "chunk_index": idx,
                "estrategia_chunking": "fixed-size",
                "chunk_texto": chunk,
                "embedding": embedding,
                "modelo": "all-MiniLM-L6-v2",
                "num_tokens": len(chunk.split()),  # aproximado
                "idioma": "es",
                "fecha_ingesta": datetime.now()
            }
            result = db.chunks.insert_one(chunk_doc)
            chunks_ids.append(result.inserted_id)
        # Actualizar el libro con los ids de los chunks
        db.libros.update_one(
            {"_id": libro_id},
            {"$set": {"chunks_ids": [str(cid) for cid in chunks_ids]}}
        )
        print(f"Libro '{titulo}': {len(chunks_ids)} chunks generados.")

def main():
    print("Cargando datos...")
    if not os.path.exists(LIBROS_JSON):
        print(f"ERROR: No se encuentra {LIBROS_JSON}")
        return
    if not os.path.exists(IMAGENES_JSON):
        print(f"ADVERTENCIA: No se encuentra {IMAGENES_JSON}. Se omitirán imágenes.")
    libros_originales = cargar_libros()
    imagenes_originales = cargar_imagenes() if os.path.exists(IMAGENES_JSON) else []
    
    print(f"Se encontraron {len(libros_originales)} libros y {len(imagenes_originales)} imágenes.")
    
    # Insertar autores
    autores_ids = insertar_autores(libros_originales)
    print(f"Autores insertados: {len(autores_ids)}")
    
    # Insertar libros
    libros_ids = insertar_libros_con_autores(libros_originales, autores_ids)
    print(f"Libros insertados: {len(libros_ids)}")
    
    # Insertar imágenes
    if imagenes_originales:
        insertar_imagenes(imagenes_originales, libros_ids)
        print("Imágenes insertadas.")
    
    # Generar chunks y embeddings
    generar_chunks_y_embeddings(libros_ids, libros_originales)
    
    print("¡Proceso completado!")

if __name__ == "__main__":
    main()