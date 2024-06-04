from typing import TYPE_CHECKING

from fastapi import APIRouter, Request, UploadFile

if TYPE_CHECKING:
    from faststream.nats.annotations import NatsBroker, ObjectStorage

text_router = APIRouter(tags=["text"], prefix="/text")


@text_router.get("/")
async def put_text(text: str, request: Request):
    broker: NatsBroker = request.state.broker
    await broker.publish(text, stream="stream", subject="texter")


@text_router.post("/file/")
async def put_file(file: UploadFile, request: Request):
    filename = file.filename
    print(filename)
    file_data = await file.read()
    broker: NatsBroker = request.state.broker
    object_storage: ObjectStorage = await broker.object_storage(bucket="storage", ttl=20)

    await object_storage.put(filename, file_data)
