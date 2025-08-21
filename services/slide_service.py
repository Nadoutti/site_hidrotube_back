from repos import slide_repo
from uuid import UUID

async def get_all_images() -> list:
    return await slide_repo.get_all_images() or []

async def get_used_slides() -> list:
    return await slide_repo.get_used_images() or []

async def add_slide(file):
    return await slide_repo.add_slide(file)

async def select_slides(img_id: UUID):
    return await slide_repo.select_slides(img_id)
