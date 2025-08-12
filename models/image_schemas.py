from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from pydantic_core.core_schema import UuidSchema


class ImageSchema(BaseModel):

    id: UUID
    img_url: str
    created_at: datetime
    used: bool
    name: str
    
    class Config:
        orm_mode = True
