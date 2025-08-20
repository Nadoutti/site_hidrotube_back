import uuid
import os
import unicodedata
import tempfile
from typing import List, Optional
from fastapi import UploadFile
from database.supabase_connection import supabase as get_supabase  # client ou factory

BUCKET = os.getenv("IMAGES_BUCKET", "images")
FOLDER = os.getenv("IMAGES_FOLDER", "noticias_img")  # pasta no bucket
SUPABASE_URL = os.getenv("SUPABASE_URL")            # https://xxxx.supabase.co

def _ascii_safe_filename(filename: str) -> str:
    base = filename.replace("/", "_").replace("\\", "_")
    base = unicodedata.normalize("NFKD", base).encode("ascii", "ignore").decode("ascii")
    return base or "file"

def _extract_public_url(pub) -> Optional[str]:
    if isinstance(pub, dict):
        data = pub.get("data")
        if isinstance(data, dict):
            return data.get("publicUrl") or data.get("signedUrl")
        return pub.get("publicUrl") or pub.get("signedUrl")
    data = getattr(pub, "data", None)
    if isinstance(data, dict):
        return data.get("publicUrl") or data.get("signedUrl")
    return None

async def upload_images_and_get_urls(files: List[UploadFile]) -> List[str]:
    if not files:
        return []

    supabase = get_supabase() if callable(get_supabase) else get_supabase
    urls: List[str] = []

    for f in files:
        raw = await f.read()
        safe = _ascii_safe_filename(f.filename)
        unique = f"{uuid.uuid4()}_{safe}"
        dest_path = f"{FOLDER}/{unique}"

        # grava temporário e passa *path* para a SDK (evita erros de encoding)
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(raw)
            tmp_path = tmp.name

        try:
            up = supabase.storage.from_(BUCKET).upload(
                path=dest_path,
                file=tmp_path,  # caminho do arquivo
                file_options={
                    "contentType": f.content_type or "application/octet-stream",
                    "upsert": False,
                },
            )
        finally:
            try:
                os.remove(tmp_path)
            except Exception:
                pass

        err = (isinstance(up, dict) and up.get("error")) or getattr(up, "error", None)
        if err:
            raise RuntimeError(f"Falha ao enviar {unique}: {err}")

        pub = supabase.storage.from_(BUCKET).get_public_url(dest_path)
        url = _extract_public_url(pub) or (
            f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{dest_path}" if SUPABASE_URL else None
        )
        if not url:
            raise RuntimeError(f"Não foi possível obter URL pública de {dest_path}")

        urls.append(url)
    print(urls)
    return urls
