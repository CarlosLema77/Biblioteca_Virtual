from fastapi import APIRouter
from fastapi.responses import JSONResponse

from models.dto import FavoriteDTO
from services.favorites_service import *

from utils.mongo_helpers import serialize_doc

router = APIRouter(
    prefix="/favoritos",
    tags=["Favoritos"]
)


@router.post("")
def favorito(f: FavoriteDTO):

    agregar(f.model_dump())

    return {
        "success": True
    }


@router.get("/{id}")
def listar(id):

    data = obtener(id)
    return JSONResponse(content=serialize_doc(data))