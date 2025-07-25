from fastapi import APIRouter
from controllers import slide_controller


router = APIRouter(prefix="/slides", tags=["slides"])


# slides routes here


# get

router.get("/")
async def get_all_images() -> list | dict:
    
    images = await slide_controller.get_all_images()
    if not images:
        return {"message": "No slides found"}
    return images

# get the used ones

@router.get("/used")
async def get_used_slides():
    return {"message": "Get used slides"}
