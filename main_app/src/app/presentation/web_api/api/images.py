from pathlib import Path
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Form, Request, UploadFile
from nats.js.api import ObjectMeta

if TYPE_CHECKING:
    from faststream.nats.annotations import NatsBroker, ObjectStorage

image_router = APIRouter(tags=["text"], prefix="/image")


# @text_router.get("/")
# async def put_text(text: str, request: Request):
#     broker: NatsBroker = request.state.broker
#     await broker.publish(text, stream="stream", subject="texter")


@image_router.post("/")
async def put_file(
    filename: Annotated[str, Form()],
    metadata: Annotated[str, Form()],
    file: UploadFile,
    request: Request,
):
    new_filename, old_filename = Path(filename), Path(file.filename)
    new_filename = new_filename.with_suffix(old_filename.suffix).name

    file_data = await file.read()
    broker: NatsBroker = request.state.broker
    object_storage: ObjectStorage = await broker.object_storage(
        bucket="storage", ttl=60
    )

    await object_storage.put(
        name=new_filename, data=file_data, meta=ObjectMeta(headers=metadata)
    )
