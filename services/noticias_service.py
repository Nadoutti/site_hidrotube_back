from typing import List, Optional, Tuple, Dict, Any
from repos.noticias_repo import NoticiaRepository as Repo


class NoticiaService:
    def __init__(self, repo: Repo | None = None):
        self.repo = repo or Repo

    # ---- validações ----
    def _validate_title(self, title: str):
        if not isinstance(title, str):
            raise ValueError("title inválido")
        if not title.strip():
            raise ValueError("title não pode ser vazio")
        if len(title) > 255:
            raise ValueError("title muito longo (<= 255)")

    # ---- criação usando URLs (vindas do storage) ----
    def create_with_urls(
        self, *, title: str, description: str, urls: List[str]
    ) -> Dict[str, Any]:
        self._validate_title(title)
        noticia = self.repo.create(title=title.strip(), description=description or "")
        # se houver galeria, adiciona
        if urls:
            updated = self.repo.add_images(noticia_id=noticia["id"], urls=urls)
            if updated:  # se repo retornou a entidade atualizada
                noticia = updated
        return noticia

    # ---- criação via JSON puro (sem upload) ----
    def create_json(
        self, *, title: str, description: str, gallery_urls: Optional[List[str]]
    ) -> Dict[str, Any]:
        return self.create_with_urls(
            title=title,
            description=description,
            urls=gallery_urls or [],
        )

    # ---- leitura ----
    def get(self, noticia_id: str) -> Optional[Dict[str, Any]]:
        if not noticia_id:
            return None
        return self.repo.get_by_id(noticia_id)

    def list(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        order_by: str = "created_at",
        order_dir: str = "desc",
        search: Optional[str] = None,
    ) -> Tuple[int, List[Dict[str, Any]]]:
        return self.repo.list(
            limit=limit,
            offset=offset,
            order_by=order_by,
            order_dir=order_dir,
            search=search,
        )

    # ---- atualização ----
    def update(
        self,
        noticia_id: str,
        *,
        title: Optional[str],
        description: Optional[str],
        gallery_urls: Optional[List[str]],
    ) -> Optional[Dict[str, Any]]:
        # valida título se vier
        if title is not None:
            self._validate_title(title)

        updated = self.repo.update(
            noticia_id,
            title=title,
            description=description,
        )
        if updated is None:
            return None

        # se a galeria foi enviada, sobrescreve completamente
        if gallery_urls is not None:
            updated = self.repo.replace_gallery(noticia_id, gallery_urls) or updated

        return updated

    # ---- exclusão ----
    def delete(self, noticia_id: str) -> bool:
        if not noticia_id:
            return False
        return self.repo.delete(noticia_id)

    # ---- imagens (incremental) ----
    def add_images(self, noticia_id: str, urls: List[str]) -> Optional[Dict[str, Any]]:
        if not noticia_id:
            return None
        if not urls:
            return self.repo.get_by_id(noticia_id)
        return self.repo.add_images(noticia_id, urls)

    def remove_image(self, image_id: str) -> bool:
        if not image_id:
            return False
        return self.repo.remove_image(image_id)
