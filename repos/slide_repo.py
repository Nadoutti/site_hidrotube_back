from sqlalchemy.orm import Session
from models.image_models import Image
from database.connection import get_db
from fastapi import Depends


# Repo functions here

# get all slides from the database

async def get_all_images(db: Session = Depends(get_db)) -> list[Image] | None:
    images = db.query(Image).all()
    if not images:
        return None

    return images



