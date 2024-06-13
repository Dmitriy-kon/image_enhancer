from contextlib import asynccontextmanager

from app.routers.api.event import minio_router
from app.routers.api.healtcheck import health_router
from app.routers.api.index import index_router
from app.routers.api.text import text_router as api_router
from app.routers.api.ws_file import ws_router
from app.routers.broker.text import nats_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# @asynccontextmanager
# async def lifespan(app: FastAPI) -> None:
#     async with (
#         nats_router.lifespan_context(app),
#     ):
#         await nats_router.broker.object_storage(bucket="storage", ttl=10)
#         yield


@nats_router.after_startup
async def after_startup(app) -> None:
    await nats_router.broker.object_storage(bucket="storage", ttl=50)


def get_lifespan() -> None:
    return nats_router.lifespan_context


def mount_styles(app: FastAPI) -> None:
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

def add_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def init_routers(app: FastAPI) -> None:
    app.include_router(nats_router)
    app.include_router(api_router)
    app.include_router(ws_router)
    app.include_router(index_router)
    app.include_router(minio_router)
    app.include_router(health_router)


def create_app() -> FastAPI:
    lifespan = get_lifespan()
    app = FastAPI(lifespan=lifespan)
    add_middlewares(app)
    mount_styles(app)
    # app = FastAPI()
    init_routers(app)

    return app
