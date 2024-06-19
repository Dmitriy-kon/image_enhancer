from typing import Annotated

from app.application.add_file_event import AddWsEvent
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

ws_router = APIRouter(tags=["ws"], prefix="/ws")


@ws_router.websocket("/file/")
async def websocket_upload_file(
    filename: str, ws: WebSocket, interactor: Annotated[AddWsEvent, Depends()]
):
    await ws.accept()
    await interactor(filename, ws)
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
