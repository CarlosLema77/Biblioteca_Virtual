from fastapi import APIRouter

from api.routes.home import router as home
from api.routes.libros import router as libros
from api.routes.autores import router as autores
from api.routes.generos import router as generos
from api.routes.imagenes import router as imagenes
from api.routes.reviews import router as reviews
from api.routes.favorites import router as favorites

router = APIRouter()

router.include_router(home)
router.include_router(libros)
router.include_router(autores)
router.include_router(generos)
router.include_router(imagenes)
router.include_router(reviews)
router.include_router(favorites)