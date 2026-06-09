"""
S: Solo se encarga de cargar el dataset a MongoDB
D: Depende de get_database() como abstracción
"""
import json
import os
from datetime import datetime, timezone
from bson import ObjectId
from pymongo import ASCENDING
from config.database import get_database


def load_json(filename: str) -> list:
    path = os.path.join("data", filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ingest_autores(db, libros: list) -> dict:
    """
    S: Solo inserta autores únicos
    Retorna un dict {nombre_autor: ObjectId} para usarlo en libros
    """
    print("👤 Insertando autores...")
    coleccion = db["autores"]

    autores_vistos = {}
    for libro in libros:
        nombre = libro["autor"]
        if nombre not in autores_vistos:
            # Verificar si ya existe en MongoDB
            existente = coleccion.find_one({"nombre": nombre})
            if existente:
                autores_vistos[nombre] = existente["_id"]
                print(f"  ⚠️  Ya existe: {nombre}")
            else:
                doc = {
                    "nombre":       nombre,
                    "nacionalidad": libro.get("nacionalidad_autor", "desconocida"),
                    "biografia":    f"Autor de {libro['titulo']}.",
                    "libros_ids":   []
                }
                result = coleccion.insert_one(doc)
                autores_vistos[nombre] = result.inserted_id
                print(f"  ✅ Insertado: {nombre}")

    print(f"\n💾 Autores procesados: {len(autores_vistos)}")
    return autores_vistos


def ingest_libros(db, libros: list, autores_map: dict) -> dict:
    """
    S: Solo inserta libros referenciando autores
    Retorna un dict {titulo: ObjectId} para usarlo en imágenes
    """
    print("\n📚 Insertando libros...")
    coleccion_libros  = db["libros"]
    coleccion_autores = db["autores"]

    libros_map = {}
    for libro in libros:
        existente = coleccion_libros.find_one({"titulo": libro["titulo"]})
        if existente:
            libros_map[libro["titulo"]] = existente["_id"]
            print(f"  ⚠️  Ya existe: {libro['titulo']}")
            continue

        autor_id = autores_map[libro["autor"]]

        doc = {
            "titulo":            libro["titulo"],
            "autor_id":          autor_id,
            "genero":            libro["genero"],
            "idioma":            libro["idioma"],
            "tipo":              libro["tipo"],
            "premium":           libro["premium"],
            "descripcion":       libro["descripcion"],
            "resenias":          [],
            "chunks_ids":        [],
            "fecha_publicacion": datetime.now(timezone.utc)
        }
        result = coleccion_libros.insert_one(doc)
        libros_map[libro["titulo"]] = result.inserted_id

        # Actualizar autor con referencia al libro
        coleccion_autores.update_one(
            {"_id": autor_id},
            {"$push": {"libros_ids": result.inserted_id}}
        )
        print(f"  ✅ Insertado: {libro['titulo']}")

    print(f"\n💾 Libros procesados: {len(libros_map)}")
    return libros_map


def ingest_imagenes(db, imagenes: list, libros_map: dict):
    """
    S: Solo inserta imágenes referenciando libros
    """
    print("\n🖼️  Insertando imágenes...")
    coleccion = db["imagenes"]

    insertadas = 0
    omitidas   = 0
    for img in imagenes:
        existente = coleccion.find_one({"nombre_archivo": img["nombre_archivo"]})
        if existente:
            omitidas += 1
            continue

        libro_id = libros_map.get(img["libro_titulo"])
        if not libro_id:
            print(f"  ❌ No se encontró libro para: {img['nombre_archivo']}")
            continue

        doc = {
            "libro_id":       libro_id,
            "nombre_archivo": img["nombre_archivo"],
            "tipo":           img["tipo"],
            "formato":        img["formato"],
            "path_local":     img["path_local"],
            "modelo_vision":  img["modelo_vision"],
            "fecha_carga":    datetime.now(timezone.utc)
        }
        coleccion.insert_one(doc)
        insertadas += 1
        print(f"  ✅ Insertada: {img['nombre_archivo']}")

    print(f"\n💾 Imágenes insertadas: {insertadas} | Omitidas: {omitidas}")


def ingest_all():
    print("🚀 Iniciando ingesta de datos...\n")
    db = get_database()

    libros   = load_json("libros.json")
    imagenes = load_json("imagenes.json")

    autores_map = ingest_autores(db, libros)
    libros_map  = ingest_libros(db, libros, autores_map)
    ingest_imagenes(db, imagenes, libros_map)

    print("\n🎉 Ingesta completada!")


if __name__ == "__main__":
    ingest_all()