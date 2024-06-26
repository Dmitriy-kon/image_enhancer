from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

index_router = APIRouter(tags=["index"], prefix="")

templates = Jinja2Templates(directory="src/app/presentation/templates")


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


@index_router.get("/ws-link")
async def websocket_link(request: Request):
    return templates.TemplateResponse(
        request=request, name="webscocket_link.html", context={"request": request}
    )
