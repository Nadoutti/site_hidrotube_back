from fastapi import HTTPException
from services import slide_service
from uuid import UUID

async def get_all_images():
    images = await slide_service.get_all_images()
    if not images:
        raise HTTPException(status_code=404, detail="No slides found")
    return images

async def get_used_slides():
    used = await slide_service.get_used_slides()
    if not used:
        raise HTTPException(status_code=404, detail="No slides found")
    return used

async def add_slide(file):
    res = await slide_service.add_slide(file)
    if not res:
        raise HTTPException(status_code=400, detail="Nao foi possivel fazer upload da imagem")
    return res

async def select_slides(img_id: UUID):
    ok = await slide_service.select_slides(img_id)
    if not ok:
        raise HTTPException(status_code=400, detail="Nao foi possivel atualizar a imagem")
    return {"message": "Imagem marcada como usada com sucesso"}
