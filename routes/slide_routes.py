from fastapi import APIRouter, HTTPException, UploadFile, File
from controllers import slide_controller


router = APIRouter(prefix="/slides", tags=["slides"])


# slides routes here


# get

router.get("/")
async def get_all_images() -> list | dict:
    
    images = await slide_controller.get_all_images()
    if not images:
        raise HTTPException(status_code=404, detail="Imagens nao encontradas")
    return images

# get the used ones

@router.get("/used")
async def get_used_slides():
    used_images = await slide_controller.get_used_slides()
    if not used_images:
        raise HTTPException(status_code=404, detail="Imagens nao encontradas")
    return 


# adicionar slides
@router.post("/")
async def add_slides(file: UploadFile = File(...)):
    response = await slide_controller.add_slide(file)

    return response


