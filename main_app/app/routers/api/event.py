from fastapi import APIRouter, Request

minio_router = APIRouter(tags=["minio-event"])


@minio_router.post("/minio-event")
async def get_event(request: Request):
    print(await request.json())
