from app.presentation.web_api.api.root import root_router
from app.presentation.web_api.broker.nats_router import nats_router
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


# @nats_router.after_startup
# async def after_startup(app) -> None:
#     await nats_router.broker.object_storage(bucket="storage", ttl=60)


def get_lifespan() -> None:
    return nats_router.lifespan_context


def init_styles(app: FastAPI) -> None:
    app.mount(
        "/static", StaticFiles(directory="src/app/presentation/static"), name="static"
    )


def init_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_routers(app: FastAPI) -> None:
    app.include_router(root_router)


def create_app() -> FastAPI:
    lifespan = get_lifespan()
    app = FastAPI(lifespan=lifespan)

    init_middlewares(app)
    init_styles(app)
    init_routers(app)

    return app
