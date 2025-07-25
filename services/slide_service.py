from repos import slide_repo
from fastapi import HTTPException

async def get_all_images() -> list:

    images = await slide_repo.get_all_images()

    if not images:
        return []
    
    return images

async def get_used_slides():
    """
    Get used slides.
    """
    return {"message": "Get used slides"}
