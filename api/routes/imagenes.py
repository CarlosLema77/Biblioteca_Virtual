from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.mongo_helpers import serialize_doc

from services.imagenes_service import get_images

from fastapi import UploadFile, File
import tempfile
import os

from services.image_search_service import search_similar_books

router = APIRouter(

    prefix="/imagenes",

    tags=["Imagenes"]

)


@router.get("/{id}")

def imagenes(id):

    data = get_images(id)
    return JSONResponse(content=serialize_doc(data))

@router.post("/search-image")
async def search_image(
    image: UploadFile = File(...)
):

    # Guardar temporalmente la imagen subida
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=os.path.splitext(image.filename)[1]
    ) as temp_file:

        temp_file.write(await image.read())
        temp_path = temp_file.name

    try:

        resultados = search_similar_books(
            image_path=temp_path,
            top_k=5
        )

        return JSONResponse(
            content=serialize_doc(resultados)
        )

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)