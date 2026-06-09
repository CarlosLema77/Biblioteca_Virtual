"""
S: Solo se encarga de preparar el dataset en formato JSON
"""
import json
import os
from datetime import datetime, timezone

LIBROS_METADATA = [
    {
        "titulo": "Don Quijote de la Mancha",
        "nombre_archivo": "don_Quijote.txt",
        "nombre_img_base": "don_quijote",
        "extension_img": "png",
        "autor": "Miguel de Cervantes Saavedra",
        "nacionalidad_autor": "española",
        "genero": ["ficción", "clásico"],
        "idioma": "es",
        "tipo": "novela",
        "premium": False,
        "fecha_publicacion": "1605-01-16",
        "descripcion": "Las aventuras del ingenioso hidalgo Don Quijote de la Mancha y su fiel escudero Sancho Panza.",
        "num_imagenes": 5
    },
    {
        "titulo": "Drácula",
        "nombre_archivo": "dracula.txt",
        "nombre_img_base": "dracula",
        "extension_img": "png",
        "autor": "Bram Stoker",
        "nacionalidad_autor": "irlandesa",
        "genero": ["terror", "gótico"],
        "idioma": "en",
        "tipo": "novela",
        "premium": False,
        "fecha_publicacion": "1897-05-26",
        "descripcion": "La historia del Conde Drácula y su intento de mudarse de Transilvania a Inglaterra.",
        "num_imagenes": 5
    },
    {
        "titulo": "El Conde de Montecristo",
        "nombre_archivo": "conde_montecristo.txt",
        "nombre_img_base": "conde_montecristo",
        "extension_img": "png",
        "autor": "Alexandre Dumas",
        "nacionalidad_autor": "francesa",
        "genero": ["suspenso", "aventura"],
        "idioma": "en",
        "tipo": "novela",
        "premium": False,
        "fecha_publicacion": "1844-08-28",
        "descripcion": "La historia de Edmond Dantès, un marinero falsamente encarcelado que busca venganza.",
        "num_imagenes": 5
    },
    {
        "titulo": "Sherlock Holmes: A Study in Scarlet",
        "nombre_archivo": "sherlock_holmes.txt",
        "nombre_img_base": "sherlock_home",
        "extension_img": "png",
        "autor": "Arthur Conan Doyle",
        "nacionalidad_autor": "escocesa",
        "genero": ["misterio", "suspenso"],
        "idioma": "en",
        "tipo": "novela",
        "premium": False,
        "fecha_publicacion": "1887-11-01",
        "descripcion": "La primera aparición del famoso detective Sherlock Holmes y el Dr. Watson.",
        "num_imagenes": 5
    },
    {
        "titulo": "Frankenstein",
        "nombre_archivo": "frankenstein.txt",
        "nombre_img_base": "Frankenstein",
        "extension_img": "png",
        "autor": "Mary Shelley",
        "nacionalidad_autor": "inglesa",
        "genero": ["terror", "ciencia ficción"],
        "idioma": "en",
        "tipo": "novela",
        "premium": False,
        "fecha_publicacion": "1818-01-01",
        "descripcion": "El científico Victor Frankenstein y la criatura que crea en un experimento.",
        "num_imagenes": 5
    },
    {
        "titulo": "Orgullo y Prejuicio",
        "nombre_archivo": "orgullo_prejuicio.txt",
        "nombre_img_base": "orgullo_prejuicio",
        "extension_img": "png",
        "autor": "Jane Austen",
        "nacionalidad_autor": "inglesa",
        "genero": ["romance", "clásico"],
        "idioma": "en",
        "tipo": "novela",
        "premium": False,
        "fecha_publicacion": "1813-01-28",
        "descripcion": "La historia de Elizabeth Bennet y su relación con el orgulloso Mr. Darcy.",
        "num_imagenes": 5
    },
    {
        "titulo": "20,000 Leguas de Viaje Submarino",
        "nombre_archivo": "20000_leguas.txt",
        "nombre_img_base": "20.000_leguas",
        "extension_img": "png",
        "autor": "Julio Verne",
        "nacionalidad_autor": "francesa",
        "genero": ["ciencia ficción", "aventura"],
        "idioma": "en",
        "tipo": "novela",
        "premium": False,
        "fecha_publicacion": "1870-01-01",
        "descripcion": "Las aventuras del Capitán Nemo a bordo del submarino Nautilus.",
        "num_imagenes": 5
    },
    {
        "titulo": "El Principito",
        "nombre_archivo": "principito.txt",
        "nombre_img_base": "principito",
        "extension_img": "png",
        "autor": "Antoine de Saint-Exupéry",
        "nacionalidad_autor": "francesa",
        "genero": ["fábula", "comedia"],
        "idioma": "en",
        "tipo": "cuento",
        "premium": False,
        "fecha_publicacion": "1943-04-06",
        "descripcion": "Un aviador conoce a un pequeño príncipe con profundas reflexiones sobre la vida.",
        "num_imagenes": 5
    },
    {
        "titulo": "La Metamorfosis",
        "nombre_archivo": "metamorfosis.txt",
        "nombre_img_base": "metamorfosis",
        "extension_img": "png",
        "autor": "Franz Kafka",
        "nacionalidad_autor": "checa",
        "genero": ["ficción", "absurdo"],
        "idioma": "en",
        "tipo": "cuento",
        "premium": False,
        "fecha_publicacion": "1915-10-15",
        "descripcion": "Gregor Samsa despierta una mañana convertido en un insecto gigante.",
        "num_imagenes": 5
    },
    {
        "titulo": "El Arte de la Guerra",
        "nombre_archivo": "arte_guerra.txt",
        "nombre_img_base": "arte_guerra",
        "extension_img": "png",
        "autor": "Sun Tzu",
        "nacionalidad_autor": "china",
        "genero": ["académico", "filosofía"],
        "idioma": "en",
        "tipo": "academico",
        "premium": False,
        "fecha_publicacion": "0500-01-01",
        "descripcion": "Tratado militar clásico chino sobre estrategia y tácticas de guerra.",
        "num_imagenes": 5
    }
]


def read_text(filename: str) -> str:
    path = os.path.join("data", "textos", filename)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def prepare_libros() -> list:
    libros = []
    for meta in LIBROS_METADATA:
        texto = read_text(meta["nombre_archivo"])
        libro = {
            "titulo":            meta["titulo"],
            "autor":             meta["autor"],
            "genero":            meta["genero"],
            "idioma":            meta["idioma"],
            "tipo":              meta["tipo"],
            "premium":           meta["premium"],
            "fecha_publicacion": meta["fecha_publicacion"],
            "descripcion":       meta["descripcion"],
            "nombre_archivo":    meta["nombre_archivo"],
            "nombre_archivo":    meta["nombre_archivo"],
            "resenias":          [],
            "chunks_ids":        []
        }
        libros.append(libro)
        print(f"  ✅ Libro preparado: {meta['titulo']}")
    return libros


def prepare_imagenes() -> list:
    imagenes = []
    for meta in LIBROS_METADATA:
        for j in range(1, meta["num_imagenes"] + 1):
            nombre_img = f"{meta['nombre_img_base']}_{j}.{meta['extension_img']}"
            path = os.path.join("data", "imagenes", nombre_img)
            if os.path.exists(path):
                imagen = {
                    "libro_titulo":   meta["titulo"],
                    "nombre_archivo": nombre_img,
                    "tipo":           "portada",
                    "formato":        meta["extension_img"],
                    "path_local":     path,
                    "modelo_vision":  "clip-vit-base-patch32",
                    "fecha_carga":    datetime.now(timezone.utc).isoformat()
                }
                imagenes.append(imagen)
                print(f"  ✅ Imagen preparada: {nombre_img}")
            else:
                print(f"  ⚠️  No encontrada: {nombre_img}")
    return imagenes


def save_json(data: list, filename: str):
    path = os.path.join("data", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Guardado: {path} ({len(data)} registros)")


def prepare_dataset():
    print("🚀 Preparando dataset...\n")

    print("📚 Procesando libros...")
    libros = prepare_libros()
    save_json(libros, "libros.json")

    print("\n🖼️  Procesando imágenes...")
    imagenes = prepare_imagenes()
    save_json(imagenes, "imagenes.json")

    print("\n🎉 Dataset listo!")
    print(f"   📚 Libros:   {len(libros)}")
    print(f"   🖼️  Imágenes: {len(imagenes)}")


if __name__ == "__main__":
    prepare_dataset()