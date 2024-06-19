from fastapi import APIRouter

from .event import minio_router
from .healtcheck import health_router
from .images import image_router
from .index import index_router
from .ws_file import ws_router

root_router = APIRouter()
root_router.include_router(minio_router)
root_router.include_router(health_router)
root_router.include_router(image_router)
root_router.include_router(index_router)
root_router.include_router(ws_router)
