from fastapi import APIRouter

health_router = APIRouter(tags=["healthcheck"], prefix="/healthcheck")


@health_router.get("")
async def health_check():
    return "OK"
