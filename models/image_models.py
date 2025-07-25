from sqlalchemy import Column, Date, String, Uuid
from ..database.connection import Base


class Image(Base):
    __tablename__ = "slide_show"

    id = Column(Uuid, primary_key=True, index=True)
    img_url = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(Date, nullable=False)

