import urllib.parse
from typing import Annotated

from app.adapters.s3.s3_client import S3Client
from app.adapters.ws.ws_client import webscocket_client
from fastapi import APIRouter, Request

s3_storage_out = S3Client(
    access_key="minioadmin",
    secret_key="minioadmin",
    endpoint_url="http://localhost:9000",
    bucket_name="storage",
)


minio_router = APIRouter(tags=["minio-event"])


@minio_router.post("/minio-event")
async def get_event(request: Request):
    data = await request.json()
    filename = data.get("Records")[0].get("s3").get("object").get("key")
    filename = urllib.parse.unquote(filename)

    ws = webscocket_client.get_file(filename)
    if not ws:
        return

    url = await s3_storage_out.get_url_for_file(filename)

    await ws.send_text(url)
    webscocket_client.remove_file(filename)
    await ws.close()
