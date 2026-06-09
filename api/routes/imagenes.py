from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.mongo_helpers import serialize_doc

from services.imagenes_service import get_images

router = APIRouter(

    prefix="/imagenes",

    tags=["Imagenes"]

)


@router.get("/{id}")

def imagenes(id):

    data = get_images(id)
    return JSONResponse(content=serialize_doc(data))