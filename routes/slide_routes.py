from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
from controllers import slide_controller
from database.connection import get_db


router = APIRouter(prefix="/slides", tags=["slides"])


# slides routes here


# get

@router.get("/")
async def get_all_images(db: Session = Depends(get_db)) -> list | dict:
    
    images = await slide_controller.get_all_images(db)
    if not images:
        raise HTTPException(status_code=404, detail="Imagens nao encontradas")
    return images

# get the used ones

@router.get("/used")
async def get_used_slides(db: Session = Depends(get_db)):
    used_images = await slide_controller.get_used_slides(db)
    if not used_images:
        raise HTTPException(status_code=404, detail="Imagens nao encontradas")
    return 


# adicionar slides
@router.post("/")
async def add_slides(file: UploadFile = File(...), db: Session = Depends(get_db)):
    response = await slide_controller.add_slide(file, db)

    return response

# selecionar_slides
@router.put("/selecionar")
async def selecionar_slides(img_ids: list[str], db: Session = Depends(get_db)):
    response = await slide_controller.selec_slides(img_ids, db)
    return response
