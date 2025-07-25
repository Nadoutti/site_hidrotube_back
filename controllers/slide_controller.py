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
    """
    Get used slides.
    """
    return {"message": "Get used slides"}
