from pathlib import Path
from typing import TYPE_CHECKING

from app.adapters.ws.ws_client import webscocket_client
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from nats.js.api import ObjectMeta

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

    webscocket_client.add_file(newfilename, ws)
    await ws.receive()
    # async for data in ws.iter_bytes():
    #     data_headers = {
    #         "grayscale": True}

    #     broker: NatsBroker = ws.state.broker
    #     object_storage: ObjectStorage = await broker.object_storage(
    #         bucket="storage", ttl=20
    #     )

    #     await object_storage.put(
    #             name=newfilename, data=data, meta=ObjectMeta(headers=data_headers))
    # try:
    #     while True:
    #         data = await ws.receive_bytes()
    #         broker: NatsBroker = ws.state.broker
    #         object_storage: ObjectStorage = await broker.object_storage(
    #             bucket="storage", ttl=20
    #         )

    #         data_headers = {
    #             "grayscale": True}
            
    #         await object_storage.put(
    #             name=newfilename, data=data, meta=ObjectMeta(headers=data_headers)
    #         )
    # except WebSocketDisconnect:
    #     print(f"disconnected {ws.client.host} {ws.client.port}")
