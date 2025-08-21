from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from controllers import slide_controller
from schemas.image_schemas import ImageSchema

router = APIRouter(prefix="/slides", tags=["slides"])

@router.get("/", response_model=List[ImageSchema])
async def get_all_images() -> list[ImageSchema]:
    return await slide_controller.get_all_images()

@router.get("/used", response_model=List[ImageSchema])
async def get_used_slides() -> list[ImageSchema]:
    return await slide_controller.get_used_slides()

@router.post("/")
async def add_slides(file: UploadFile = File(...)):
    return await slide_controller.add_slide(file)

@router.put("/selecionar")
async def selecionar_slides(img_id: UUID = Query(...)):
    return await slide_controller.select_slides(img_id)
