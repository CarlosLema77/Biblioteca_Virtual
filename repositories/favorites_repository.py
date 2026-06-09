from config.database import get_database
from bson import ObjectId

db = get_database()


def add_favorite(data):
    # Convertir usuario_id a ObjectId si es string
    usuario_id = data["usuario_id"]
    if isinstance(usuario_id, str):
        usuario_id = ObjectId(usuario_id)
    
    db.usuarios.update_one(
        {"_id": usuario_id},
        {"$push": {"favoritos": data["libro_id"]}}
    )
    return True


def get_favorites(user):
    # Convertir user a ObjectId si es string
    if isinstance(user, str):
        user = ObjectId(user)
    
    usuario = db.usuarios.find_one({"_id": user})
    favoritos = usuario.get("favoritos", []) if usuario else []
    
    # Convertir cada favorito a string (por si vienen como ObjectId)
    return [str(fav) for fav in favoritos]