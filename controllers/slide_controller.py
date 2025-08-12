from fastapi import HTTPException
from sqlalchemy.orm import Session
from services import slide_service


# get all slides
async def get_all_images(db: Session):
    
    images = await slide_service.get_all_images(db)
    if len(images) == 0:
        raise HTTPException(status_code=404, detail="No slides found")

    return images


# get the used ones
async def get_used_slides(db: Session):

    used_images = await slide_service.get_used_slides(db)

    if len(used_images) == 0:
        raise HTTPException(status_code=404, detail="No slides found")

    return used_images

async def add_slide(file, db: Session):

    response = await slide_service.add_slide(file, db)

    if not response:
        raise HTTPException(status_code=400, detail="Nao foi possivel fazer upload da imagem")

    return response

async def selec_slides(img_id, db: Session):


    response = await slide_service.selec_slides(img_id, db)
    if not response:
        raise HTTPException(status_code=400, detail="Deu problema ein")
    return response


