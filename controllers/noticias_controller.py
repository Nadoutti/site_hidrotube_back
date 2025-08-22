# app/controllers/noticia_controller.py
from typing import List, Optional
from fastapi import HTTPException, UploadFile
from schemas.Noticias import (
    NoticiaCreate, NoticiaUpdate, NoticiaRead, NoticiaList, NoticiaAddImages, NoticiaImgRead
)
from services.noticias_service import NoticiaService
from services.storage_service import upload_images_and_get_urls


class NoticiaController:
    def __init__(self, service: NoticiaService | None = None):
        self.service = service or NoticiaService()

    # ---------- helpers ----------
    def _to_read(self, data: dict) -> NoticiaRead:
        images = data.get("images") or []
        cover = images[0]["img_url"] if images else None
        return NoticiaRead(
            id=data["id"],
            title=str(data.get("title") or ""),
            description=str(data.get("description") or ""),
            cover_url=cover,
            images=[NoticiaImgRead(id=img["id"], img_url=img["img_url"]) for img in images],
        )

    # ---------- JSON (sem upload) ----------
    def create(self, payload: NoticiaCreate) -> NoticiaRead:
        try:
            created = self.service.create_json(
                title=payload.title,
                description=payload.description,
                gallery_urls=payload.gallery_urls,
            )
            return self._to_read(created)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar notícia: {e}")

    # ---------- multipart (upload) ----------
    async def create_with_files(self, title: str, description: str, files: List[UploadFile]) -> NoticiaRead:
        if not files:
            raise HTTPException(status_code=400, detail="Envie ao menos uma imagem em files[]")
        try:
            urls = await upload_images_and_get_urls(files)  # sobe para o bucket e retorna URLs
            created = self.service.create_with_urls(
                title=title,
                description=description,
                urls=urls,
            )
            return self._to_read(created)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar notícia: {e}")

    # ---------- listagem ----------
    def list(
        self,
        *,
        limit: int,
        offset: int,
        order_by: str,
        order_dir: str,
        search: Optional[str],
    ) -> NoticiaList:
        total, items = self.service.list(
            limit=limit,
            offset=offset,
            order_by=order_by,
            order_dir=order_dir,
            search=search,
        )
        return NoticiaList(
            total=total,
            items=[self._to_read(n) for n in items],
        )

    # ---------- obter por id ----------
    def get(self, noticia_id: str) -> NoticiaRead:
        data = self.service.get(noticia_id)
        if not data:
            raise HTTPException(status_code=404, detail="Notícia não encontrada")
        return self._to_read(data)

    # ---------- atualizar ----------
    def update(self, noticia_id: str, payload: NoticiaUpdate) -> NoticiaRead:
        try:
            updated = self.service.update(
                noticia_id=noticia_id,
                title=payload.title,
                description=payload.description,
                gallery_urls=payload.gallery_urls,
            )
            if not updated:
                raise HTTPException(status_code=404, detail="Notícia não encontrada")
            return self._to_read(updated)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar notícia: {e}")

    # ---------- deletar ----------
    def delete(self, noticia_id: str) -> None:
        ok = self.service.delete(noticia_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Notícia não encontrada")

    # ---------- imagens ----------
    def add_images(self, noticia_id: str, payload: NoticiaAddImages) -> NoticiaRead:
        updated = self.service.add_images(noticia_id, [str(u) for u in payload.image_urls])
        if not updated:
            raise HTTPException(status_code=404, detail="Notícia não encontrada")
        return self._to_read(updated)

    def remove_image(self, image_id: str) -> None:
        ok = self.service.remove_image(image_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Imagem não encontrada")
