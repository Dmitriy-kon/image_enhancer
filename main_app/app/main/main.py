from contextlib import asynccontextmanager

from app.routers.api.text import text_router as api_router
from app.routers.broker.text import nats_router
from fastapi import FastAPI

# @asynccontextmanager
# async def lifespan(app: FastAPI) -> None:
#     async with (
#         nats_router.lifespan_context(app),
#     ):
#         await nats_router.broker.object_storage(bucket="storage", ttl=10)
#         yield


@nats_router.after_startup
async def after_startup(app) -> None:
    await nats_router.broker.object_storage(bucket="storage", ttl=10)

def get_lifespan() -> None:
    return nats_router.lifespan_context


def init_routers(app: FastAPI) -> None:
    app.include_router(nats_router)
    app.include_router(api_router)


def create_app() -> FastAPI:
    lifespan = get_lifespan()
    app = FastAPI(lifespan=lifespan)
    # app = FastAPI()
    init_routers(app)

    return app
