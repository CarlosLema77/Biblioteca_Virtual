from fastapi import APIRouter

from models.dto import ReviewDTO

from services.reviews_service import *

router=APIRouter(

prefix="/reviews",

tags=["Reviews"]

)


@router.post("/{id}")

def review(

id,

r:ReviewDTO

):

    publicar(

        id,

        r.model_dump()

    )

    return {

        "success":True

    }