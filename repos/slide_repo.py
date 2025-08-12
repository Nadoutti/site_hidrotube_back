from sqlalchemy import String
from sqlalchemy.orm import Session
from datetime import datetime
from models.image_models import Image
from database.connection import get_db
from database.supabase_connection import supabase
import uuid


# Repo functions here

# get all slides from the database

async def get_all_images(db: Session) -> list[Image] | None:
    images = db.query(Image).all()
    if not images:
        return None

    return images


async def get_used_images(db: Session) -> list[Image] | None:

    used_images = db.query(Image).filter(Image.used == True).all()

    if not used_images:
        return None

    return used_images

async def add_slide(file, db: Session):

    contents = await file.read()
    filename = f"{uuid.uuid4()}_{file.filename}"

    res = supabase.storage.from_('images').upload(
        path=f"slides/{ filename }",
        file=contents,
        file_options={"content-type": file.content_type},
    )

    if not res:
        return None

    public_url = supabase.storage.from_('images/slides').get_public_url(filename)

    new_image = Image(id=uuid.uuid4(), created_at=datetime.now(), img_url=public_url, used=False, name=filename)

    db.add(new_image)
    db.commit()

    added_image = db.query(Image).filter(Image.name == filename).first()

    if not added_image:
        return {"error": f"Não foi ṕossivel adicionara aimagem {filename}"}


    return {"message": f"Imagem adicionada com sucesso!"}


async def selec_slides(img_id, db: Session):
    count = 0

    image = db.query(Image).filter(Image.id == img_id).first()

    if not image:
        return None
    
    print(image.id)

    image.used = True
    print(image.used)

    db.commit()

    return {"message": f"nao foi possivel atualizar todas as imagens: {count}"}

