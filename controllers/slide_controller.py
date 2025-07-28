from fastapi import HTTPException
from services import slide_service


# get all slides
async def get_all_images():
    
    images = await slide_service.get_all_images()
    if len(images) == 0:
        raise HTTPException(status_code=404, detail="No slides found")

    return images


# get the used ones
async def get_used_slides():

    used_images = await slide_service.get_used_slides()

    if len(used_images) == 0:
        raise HTTPException(status_code=404, detail="No slides found")

    return used_images

async def add_slide(file):

    response = await slide_service.add_slide(file)

    if not response:
        raise HTTPException(status_code=400, detail="Nao foi possivel fazer upload da imagem")
