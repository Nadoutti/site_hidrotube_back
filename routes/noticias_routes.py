# routes/noticias_routes.py
from typing import Optional, List, Annotated
from fastapi import APIRouter, UploadFile, File, Form
from controllers.noticias_controller import NoticiaController
from schemas.Noticias import (
    NoticiaCreate, NoticiaUpdate, NoticiaRead, NoticiaList, NoticiaAddImages
)

router = APIRouter(prefix="/noticias", tags=["noticias"])
controller = NoticiaController()

def _dec_bytes(b: bytes) -> str:
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            continue
    return b.decode("utf-8", "replace")

# ---------- criação com upload ----------
@router.post("/upload", response_model=NoticiaRead)
async def create_noticia_with_files(
    title_b: Annotated[bytes, Form(...)],
    description_b: Annotated[bytes, Form(...)],
    files: List[UploadFile] = File(...),
):
    title = _dec_bytes(title_b)
    description = _dec_bytes(description_b)
    return await controller.create_with_files(title, description, files)

# ---------- CRUD via JSON ----------
@router.post("", response_model=NoticiaRead)
def create_noticia(payload: NoticiaCreate):
    return controller.create(payload)

@router.get("", response_model=NoticiaList)
def list_noticias(
    limit: int = 20,
    offset: int = 0,
    order_by: str = "created_at",
    order_dir: str = "desc",
    search: Optional[str] = None,
):
    return controller.list(
        limit=limit,
        offset=offset,
        order_by=order_by,
        order_dir=order_dir,
        search=search,
    )

@router.get("/{noticia_id}", response_model=NoticiaRead)
def get_noticia(noticia_id: str):
    return controller.get(noticia_id)

@router.put("/{noticia_id}", response_model=NoticiaRead)
def update_noticia(noticia_id: str, payload: NoticiaUpdate):
    return controller.update(noticia_id, payload)

@router.delete("/{noticia_id}", status_code=204)
def delete_noticia(noticia_id: str):
    controller.delete(noticia_id)
    return None

# ---------- imagens ----------
@router.post("/{noticia_id}/images", response_model=NoticiaRead)
def add_images(noticia_id: str, payload: NoticiaAddImages):
    return controller.add_images(noticia_id, payload)

@router.delete("/images/{image_id}", status_code=204)
def remove_image(image_id: str):
    controller.remove_image(image_id)
    return None
