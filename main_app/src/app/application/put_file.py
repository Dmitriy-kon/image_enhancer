import json
from typing import TYPE_CHECKING

from app.domain.entities import Image
from fastapi import Request, UploadFile
from nats.js.api import ObjectMeta

if TYPE_CHECKING:
    from faststream.nats.annotations import NatsBroker, ObjectStorage


class PutImagetoBroker:
    # def __init__(self, broker):
    #     self.broker = broker

    async def __call__(
        self, new_filename: str, metadata: str, file: UploadFile, request: Request
    ):
        convert_data = json.loads(metadata)
        image = Image.create(file.filename, convert_data=convert_data)
        image.get_updated_name(new_filename)

        file_data = await file.read()

        broker: NatsBroker = request.state.broker
        object_storage: ObjectStorage = await broker.object_storage(
            bucket="storage", ttl=60
        )
        print(image.name)
        await object_storage.put(
            name=image.name, data=file_data, meta=ObjectMeta(headers=image.convert_data)
        )
