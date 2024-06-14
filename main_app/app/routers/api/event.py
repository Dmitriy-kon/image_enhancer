from pprint import pprint

from app.adapters.ws.ws_client import webscocket_client
from app.s3.s3 import S3Client
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
    ws = webscocket_client.get_file(filename)

    url = await s3_storage_out.get_url_for_file(filename)
    await ws.send_text(url)
    print(url)
    

    # pprint(data.get("Records")[0].get("s3").get("object").get("key"))
