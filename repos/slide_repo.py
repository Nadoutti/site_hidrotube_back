# repos/slide_repo.py
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4, UUID
from typing import Optional, List, Dict

# Importa a FUNÇÃO, renomeando para evitar confusão de nomes
from database.supabase_connection import supabase as supabase_factory

TABLE = "slide_show"     # sua tabela no Supabase
BUCKET = "images"    # seu bucket no Storage
FOLDER = "slides"    # pasta dentro do bucket

def _sb():
    # Sempre que precisar, pega o client chamando a função
    return supabase_factory()

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

async def get_all_images() -> Optional[List[Dict]]:
    sb = _sb()
    res = sb.table(TABLE).select("*").order("created_at", desc=True).execute()
    data = res.data or []
    return data or None

async def get_used_images() -> Optional[List[Dict]]:
    sb = _sb()
    res = sb.table(TABLE).select("*").eq("used", True).order("created_at", desc=True).execute()
    data = res.data or []
    return data or None

async def add_slide(file) -> Optional[Dict]:
    sb = _sb()

    contents: bytes = await file.read()
    ext = Path(file.filename).suffix.lower()  # mantém .png/.jpg etc
    filename = f"{uuid4()}{ext}"
    storage_path = f"{FOLDER}/{filename}"

    # Upload no Storage (bucket 'images', caminho 'slides/<uuid>.<ext>')
    up = sb.storage.from_(BUCKET).upload(
        path=storage_path,
        file=contents,
        file_options={"content-type": file.content_type},
    )

    # Trata erro de forma defensiva (dependendo da versão pode vir dict)
    if not up or (isinstance(up, dict) and up.get("error")):
        return None

    public_url = sb.storage.from_(BUCKET).get_public_url(storage_path)

    row_id = str(uuid4())
    new_row = {
        "id": row_id,
        "name": filename,
        "img_url": public_url,
        "used": False,
        "created_at": _now_iso(),
    }

    ins = sb.table(TABLE).insert(new_row).execute()
    if not ins.data:
        # (Opcional) rollback do arquivo subido:
        # sb.storage.from_(BUCKET).remove([storage_path])
        return None
    return {"message": "Imagem adicionada com sucesso!", "id": row_id, "url": public_url}

async def select_slides(img_id: UUID) -> bool:
    sb = _sb()
    upd = sb.table(TABLE).update({"used": True}).eq("id", str(img_id)).execute()
    return bool(upd.data)
