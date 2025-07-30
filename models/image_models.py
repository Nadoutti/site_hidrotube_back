from sqlalchemy import Boolean, Date, String, Uuid, null
from sqlalchemy.orm import Mapped, MappedColumn, mapped_column
from database.connection import Base


class Image(Base):
    __tablename__ = "slide_show"

    id: Mapped[str] = mapped_column(Uuid, nullable=False, primary_key=True, index=True)
    img_url: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[str] = mapped_column(Date, nullable=False)
    used: Mapped[bool] = mapped_column(Boolean, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)

