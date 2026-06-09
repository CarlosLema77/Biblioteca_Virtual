from fastapi import APIRouter
from fastapi.responses import JSONResponse
from repositories.home_repository import home as get_home_data
from utils.mongo_helpers import serialize_doc

router = APIRouter(
    prefix="/home",
    tags=["Home"]
)

@router.get("")
def home():
    data = get_home_data()
    # Retornar directamente con JSONResponse (evita problemas de serialización)
    return JSONResponse(content=serialize_doc(data))