from fastapi import APIRouter
from fastapi.responses import JSONResponse

from utils.mongo_helpers import serialize_doc

from services.autores_service import (
    obtener_autores,
    obtener_autor,
    obtener_autor_completo
)

router = APIRouter(
    prefix="/autores",
    tags=["Autores"]
)


@router.get("")
def listar():

    data = obtener_autores()
    return JSONResponse(content=serialize_doc(data))


@router.get("/{id}")
def detalle(id):

    data = obtener_autor(id)
    return JSONResponse(content=serialize_doc(data))


@router.get("/detalle/{id}")
def detalle(id):

    data = obtener_autor_completo(id)
    return JSONResponse(content=serialize_doc(data))