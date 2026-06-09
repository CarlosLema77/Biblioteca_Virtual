from fastapi import APIRouter
from config.database import get_database

router = APIRouter(
    prefix="/generos",
    tags=["Generos"]
)

db = get_database()


@router.get("")
def listar_generos():

    generos = db.libros.distinct("genero")

    return generos