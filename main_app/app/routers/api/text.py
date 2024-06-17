from pathlib import Path
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Form, Request, UploadFile
from nats.js.api import ObjectMeta

if TYPE_CHECKING:
    from faststream.nats.annotations import NatsBroker, ObjectStorage

text_router = APIRouter(tags=["text"], prefix="/text")


@text_router.get("/")
async def put_text(text: str, request: Request):
    broker: NatsBroker = request.state.broker
    await broker.publish(text, stream="stream", subject="texter")


@text_router.post("/file/")
async def put_file(
    filename: Annotated[str, Form()],
    metadata: Annotated[str, Form()],
    file: UploadFile,
    request: Request,
):
    if filename:
        filename_suffix = Path(file.filename).suffix
        filename = f"{filename}{filename_suffix}"
    else:
        filename = file.filename

    print(filename)
    # data_headers = file.headers
    print(file.headers)
    print(metadata)

    data_headers = {"grayscale": True}

    file_data = await file.read()
    broker: NatsBroker = request.state.broker
    object_storage: ObjectStorage = await broker.object_storage(
        bucket="storage", ttl=20
    )

    await object_storage.put(
        name=filename, data=file_data, meta=ObjectMeta(headers=metadata)
    )
