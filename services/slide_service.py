from sqlalchemy.orm import Session
from repos import slide_repo
from fastapi import HTTPException

async def get_all_images(db: Session) -> list:

    images = await slide_repo.get_all_images(db)

    if not images:
        return []
    
    return images

async def get_used_slides(db: Session) -> list:

    used_images = await slide_repo.get_used_images(db)

    if not used_images:
        return []
    
    return used_images

async def add_slide(file, db: Session):

    response = await slide_repo.add_slide(file, db)

    return response


async def selec_slides(img_ids, db: Session):

    response = await slide_repo.selec_slides(img_ids, db)

    return response

