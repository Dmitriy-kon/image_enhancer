from typing import TYPE_CHECKING

from fastapi import APIRouter, Request, UploadFile
from fastapi.templating import Jinja2Templates

if TYPE_CHECKING:
    from faststream.nats.annotations import NatsBroker, ObjectStorage

index_router = APIRouter(tags=["index"], prefix="")

templates = Jinja2Templates(directory="app/templates")


@index_router.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"request": request}
    )

@index_router.get("/ws")
async def websocket_upload(request: Request):
    return templates.TemplateResponse(
        request=request, name="webscocket.html", context={"request": request}
    )
