from datetime import datetime
from typing import List
from sqlalchemy import Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import text as sqltext
from database.connection import Base

class Noticia(Base):
    __tablename__ = "noticias"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True),
                                    primary_key=True,
                                    server_default=sqltext("gen_random_uuid()"))
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now(),
                                                 nullable=False)

    images: Mapped[List["NoticiaImg"]] = relationship(
        "NoticiaImg",
        back_populates="noticia",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

class NoticiaImg(Base):
    __tablename__ = "noticia_img"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True),
                                    primary_key=True,
                                    server_default=sqltext("gen_random_uuid()"))
    noticia_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("noticias.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    img_url: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now(),
                                                 nullable=False)

    noticia = relationship("Noticia", back_populates="images")
