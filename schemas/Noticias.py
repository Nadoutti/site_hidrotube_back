from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, AnyHttpUrl, field_validator

class NoticiaImgRead(BaseModel):
    id: UUID
    img_url: AnyHttpUrl
    class Config:
        from_attributes = True

class NoticiaRead(BaseModel):
    id: UUID
    title: str
    description: str
    # capa = primeira imagem (computado na resposta)
    cover_url: Optional[AnyHttpUrl] = None
    images: List[NoticiaImgRead] = []
    class Config:
        from_attributes = True

class NoticiaList(BaseModel):
    total: int
    items: List[NoticiaRead]

class NoticiaCreate(BaseModel):
    title: str
    description: str
    # criação via JSON (sem upload) – opcionalmente já passa urls
    gallery_urls: Optional[List[AnyHttpUrl]] = None

    @field_validator("gallery_urls")
    @classmethod
    def dedup_urls(cls, v):
        if v:
            return list(dict.fromkeys(v))
        return v

class NoticiaUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    # se fornecido, sobrescreve toda a galeria
    gallery_urls: Optional[List[AnyHttpUrl]] = None

    @field_validator("gallery_urls")
    @classmethod
    def dedup_urls(cls, v):
        if v:
            return list(dict.fromkeys(v))
        return v

class NoticiaAddImages(BaseModel):
    image_urls: List[AnyHttpUrl]
    @field_validator("image_urls")
    @classmethod
    def dedup_urls(cls, v):
        return list(dict.fromkeys(v)) if v else v
