from pathlib import Path
from typing import TYPE_CHECKING

from fastapi import APIRouter, Request, UploadFile, WebSocket, WebSocketDisconnect

if TYPE_CHECKING:
    from faststream.nats.annotations import NatsBroker, ObjectStorage

ws_router = APIRouter(tags=["ws"], prefix="/ws")


@ws_router.websocket("/")
async def websocket_upload(name: str, ws: WebSocket):
    print(name)
    await ws.accept()

    try:
        async for data in ws.iter_text():
            await ws.send_text(f"Message text was: {data}")
        # while True:
        #     data = await ws.receive_text()
        #     await ws.send_text(data)
    except WebSocketDisconnect:
        pass


@ws_router.websocket("/file/")
async def websocket_upload_file(filename: str, ws: WebSocket):
    await ws.accept()

    new_filename, old_filename = (Path(i) for i in filename.split(":"))
    newfilename = new_filename.with_suffix(old_filename.suffix).name

    async for data in ws.iter_bytes():
        await ws.send_text(newfilename)
        await ws.send_bytes(data)
    # try:
    # while True:
    #     data = await ws.receive_text()
    #     await ws.send_text(data)
    # except WebSocketDisconnect:
    #     pass


# @text_router.post("/file/")
# async def put_file(file: UploadFile, request: Request):
#     filename = file.filename
#     file_data = await file.read()
#     broker: NatsBroker = request.state.broker
#     object_storage: ObjectStorage = await broker.object_storage(bucket="storage", ttl=20)

#     await object_storage.put(filename, file_data)
