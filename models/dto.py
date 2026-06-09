from pydantic import BaseModel
from typing import Optional


class BookDTO(BaseModel):

    titulo: str

    descripcion: Optional[str] = None

    genero: list

    idioma: str

    tipo: str

    premium: bool = False


class AuthorDTO(BaseModel):

    nombre: str

    nacionalidad: str

    biografia: Optional[str] = None


class ReviewDTO(BaseModel):

    usuario: str

    comentario: str

    estrellas: int


class FavoriteDTO(BaseModel):

    usuario_id: str

    libro_id: str