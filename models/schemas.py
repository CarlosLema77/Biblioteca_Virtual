"""
S: Solo contiene las definiciones de esquemas de validación
O: Para agregar un nuevo esquema, solo se agrega una nueva variable
"""

SCHEMA_USUARIOS = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["nombre", "email", "password_hash", "fecha_registro"],
        "properties": {
            "nombre":         { "bsonType": "string" },
            "email":          { "bsonType": "string" },
            "password_hash":  { "bsonType": "string" },
            "fecha_registro": { "bsonType": "date" },
            "favoritos":      { "bsonType": "array" },
            "historial":      { "bsonType": "array" },
            "consultas_rag":  { "bsonType": "array" }
        }
    }
}

SCHEMA_LIBROS = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["titulo", "autor_id", "genero", "idioma", "tipo"],
        "properties": {
            "titulo":             { "bsonType": "string" },
            "autor_id":           { "bsonType": "objectId" },
            "genero":             { "bsonType": "array" },
            "idioma":             { "bsonType": "string" },
            "tipo": {
                "bsonType": "string",
                "enum": ["novela", "articulo", "academico", "cuento"]
            },
            "premium":            { "bsonType": "bool" },
            "portada_id":         { "bsonType": "objectId" },
            "descripcion":        { "bsonType": "string" },
            "resenias":           { "bsonType": "array" },
            "chunks_ids":         { "bsonType": "array" }
        }
    }
}

SCHEMA_AUTORES = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["nombre", "nacionalidad"],
        "properties": {
            "nombre":          { "bsonType": "string" },
            "nacionalidad":    { "bsonType": "string" },
            "biografia":       { "bsonType": "string" },
            "fecha_nacimiento":{ "bsonType": "date" },
            "libros_ids":      { "bsonType": "array" }
        }
    }
}

SCHEMA_IMAGENES = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["libro_id", "tipo", "formato", "fecha_carga"],
        "properties": {
            "libro_id":         { "bsonType": "objectId" },
            "tipo": {
                "bsonType": "string",
                "enum": ["portada", "ilustracion"]
            },
            "url":              { "bsonType": "string" },
            "path_local":       { "bsonType": "string" },
            "formato":          { "bsonType": "string" },
            "resolucion":       { "bsonType": "string" },
            "embedding_visual": { "bsonType": "array" },
            "modelo_vision":    { "bsonType": "string" },
            "fecha_carga":      { "bsonType": "date" }
        }
    }
}

SCHEMA_CHUNKS = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["doc_id", "chunk_index", "estrategia_chunking", 
                     "chunk_texto", "modelo", "fecha_ingesta"],
        "properties": {
            "doc_id":               { "bsonType": "objectId" },
            "chunk_index":          { "bsonType": "int" },
            "estrategia_chunking": {
                "bsonType": "string",
                "enum": ["fixed-size", "sentence-aware", "semantic"]
            },
            "chunk_texto":          { "bsonType": "string" },
            "embedding":            { "bsonType": "array" },
            "modelo":               { "bsonType": "string" },
            "num_tokens":           { "bsonType": "int" },
            "idioma":               { "bsonType": "string" },
            "fecha_ingesta":        { "bsonType": "date" }
        }
    }
}