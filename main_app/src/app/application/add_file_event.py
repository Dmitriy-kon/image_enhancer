from app.adapters.ws.ws_client import webscocket_client
from app.domain.entities import Image
from fastapi import WebSocket


class AddWsEvent:
    # def __init__(self, broker):
    #     self.broker = broker

    async def __call__(self, filename: str, ws: WebSocket):
        new_filename, old_filename = (i for i in filename.split(":"))
        image = Image.create(old_filename)
        image.get_updated_name(new_filename)

        webscocket_client.add_file(image.name, ws)
