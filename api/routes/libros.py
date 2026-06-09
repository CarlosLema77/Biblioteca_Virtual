from fastapi import APIRouter
from models.dto import BookDTO
from fastapi.responses import JSONResponse
from utils.mongo_helpers import serialize_doc

from services.libros_service import (
    obtener_libros,
    obtener_libro,
    obtener_destacados,
    obtener_libros_genero,
    obtener_libros_autor,
    obtener_libro_completo,
    crear_libro,
    editar_libro,
    borrar_libro
)

router = APIRouter(
    prefix="/libros",
    tags=["Libros"]
)


@router.get("")
def listar_libros():

    data = obtener_libros()
    return JSONResponse(content=serialize_doc(data))


@router.get("/destacados")
def destacados():

    data = obtener_destacados()
    return JSONResponse(content=serialize_doc(data))

@router.get("/detalle/{id}")
def detalle_completo(id):

    data = obtener_libro_completo(id)
    return JSONResponse(content=serialize_doc(data))


@router.get("/{id}")
def detalle(id):

    data = obtener_libro(id)
    return JSONResponse(content=serialize_doc(data))


@router.get("/autor/{id}")

def libros_autor(id):

    data = obtener_libros_autor(id)
    return JSONResponse(content=serialize_doc(data))


@router.get("/genero/{genero}")

def libros_genero(genero):

    data = obtener_libros_genero(genero)
    return JSONResponse(content=serialize_doc(data))

@router.post("")

def crear(book:BookDTO):

    return {

        "id":crear_libro(book.model_dump())

    }
    
@router.put("/{id}")

def editar(id,book:BookDTO):

    editar_libro(

        id,

        book.model_dump()

    )

    return {

        "success":True

    }
    
@router.delete("/{id}")

def eliminar(id):

    borrar_libro(id)

    return {

        "success":True

    }