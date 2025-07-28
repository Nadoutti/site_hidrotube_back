from repos import slide_repo
from fastapi import HTTPException

async def get_all_images() -> list:

    images = await slide_repo.get_all_images()

    if not images:
        return []
    
    return images

async def get_used_slides() -> list:

    used_images = await slide_repo.get_used_images()

    if not used_images:
        return []
    
    return used_images

async def add_slide(file):

    response = await slide_repo.add_slide(file)

    return response
