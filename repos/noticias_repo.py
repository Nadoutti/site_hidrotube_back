# app/repositories/noticia_repository_supabase.py
from typing import List, Optional, Tuple, Dict, Any
from supabase import Client
from database.supabase_connection import supabase as get_supabase

TBL = "noticias"
TBL_IMG = "noticia_img"

def _sb() -> Client:
    return get_supabase() if callable(get_supabase) else get_supabase

def _normalize(row: Dict[str, Any]) -> Dict[str, Any]:
    imgs = row.get("noticia_img") or row.get("images") or []
    return {
        "id": str(row.get("id")),
        "title": row.get("title"),
        "description": row.get("description"),
        "created_at": row.get("created_at"),
        "images": [
            {"id": str(i.get("id")), "img_url": i.get("img_url"), "created_at": i.get("created_at")}
            for i in (imgs or [])
        ],
    }

class NoticiaRepository:
    # -------- CREATE --------
    @staticmethod
    def create(*, title: str, description: str) -> Dict[str, Any]:
        sb = _sb()
        res = sb.table(TBL).insert(
            {"title": title, "description": description},
            returning="representation",   # << retorna a linha inserida
        ).execute()
        if not res.data:
            # como fallback, faz um select (raro precisar)
            raise RuntimeError("Falha ao inserir notícia")
        row = res.data[0]
        # anexa galeria vazia
        row["noticia_img"] = []
        return _normalize(row)

    # -------- READ --------
    @staticmethod
    def get_by_id(noticia_id: str) -> Optional[Dict[str, Any]]:
        sb = _sb()
        res = (
            sb.table(TBL)
            .select("id, title, description, created_at, noticia_img(id, img_url, created_at)")
            .eq("id", noticia_id)
            .single()
            .execute()
        )
        if getattr(res, "data", None) is None:
            return None
        return _normalize(res.data)

    @staticmethod
    def list(
        *, limit: int = 20, offset: int = 0, order_by: str = "created_at",
        order_dir: str = "desc", search: Optional[str] = None
    ) -> Tuple[int, List[Dict[str, Any]]]:
        sb = _sb()
        q = sb.table(TBL).select(
            "id, title, description, created_at, noticia_img(id, img_url, created_at)",
            count="exact"
        )
        if search:
            q = q.ilike("title", f"%{search}%")
        desc = order_dir.lower() == "desc"
        order_col = order_by if order_by in ("created_at", "title", "description") else "created_at"
        q = q.order(order_col, desc=desc)
        q = q.range(offset, offset + max(0, limit) - 1)
        res = q.execute()
        items = [_normalize(r) for r in (res.data or [])]
        total = int(getattr(res, "count", 0) or 0)
        return total, items

    # -------- UPDATE --------
    @staticmethod
    def update(noticia_id: str, *, title: Optional[str], description: Optional[str]) -> Optional[Dict[str, Any]]:
        sb = _sb()
        payload: Dict[str, Any] = {}
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        if not payload:
            return NoticiaRepository.get_by_id(noticia_id)

        # em v2 não encadeie .select após update; use returning ou busque depois
        res = sb.table(TBL).update(payload).eq("id", noticia_id).execute()
        # se quiser retorno imediato da linha atualizada:
        # res = sb.table(TBL).update(payload, returning="representation").eq("id", noticia_id).execute()
        # row = res.data[0] if res.data else None
        # return _normalize(row) if row else None

        # padrão: busca completa (com galeria) depois
        return NoticiaRepository.get_by_id(noticia_id)

    # -------- DELETE --------
    @staticmethod
    def delete(noticia_id: str) -> bool:
        sb = _sb()
        # se não tiver ON DELETE CASCADE no DB, limpe as imagens primeiro
        sb.table(TBL_IMG).delete().eq("noticia_id", noticia_id).execute()
        res = sb.table(TBL).delete().eq("id", noticia_id).execute()
        # sucesso se não deu erro; PostgREST nem sempre retorna linhas deletadas
        return True

    # -------- GALLERY --------
    @staticmethod
    def add_images(noticia_id: str, urls: List[str]) -> Optional[Dict[str, Any]]:
        if not urls:
            return NoticiaRepository.get_by_id(noticia_id)
        sb = _sb()
        rows = [{"noticia_id": noticia_id, "img_url": u} for u in urls]
        sb.table(TBL_IMG).insert(rows).execute()
        return NoticiaRepository.get_by_id(noticia_id)

    @staticmethod
    def replace_gallery(noticia_id: str, urls: List[str]) -> Optional[Dict[str, Any]]:
        sb = _sb()
        sb.table(TBL_IMG).delete().eq("noticia_id", noticia_id).execute()
        if urls:
            rows = [{"noticia_id": noticia_id, "img_url": u} for u in urls]
            sb.table(TBL_IMG).insert(rows).execute()
        return NoticiaRepository.get_by_id(noticia_id)

    @staticmethod
    def remove_image(image_id: str) -> bool:
        sb = _sb()
        sb.table(TBL_IMG).delete().eq("id", image_id).execute()
        return True
