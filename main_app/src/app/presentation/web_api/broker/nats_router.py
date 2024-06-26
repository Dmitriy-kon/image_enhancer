import asyncio
from typing import Annotated

from app.main.config import config
from fastapi import Depends
from faststream.nats import JStream, ObjWatch
from faststream.nats.annotations import ObjectStorage
from faststream.nats.fastapi import NatsRouter

nats_router = NatsRouter(config.nats_config.broker_url)
broker = nats_router.broker


@nats_router.after_startup
async def after_startup(app) -> None:
    await nats_router.broker.object_storage(
        bucket=config.nats_config.bucket_name, ttl=config.nats_config.ttl
    )


# @nats_router.subscriber(stream="stream", subject="texter", deliver_policy="new")
# async def put_text(text: str):
#     print(f"{text}, from broker")


# def write_file(filename: str, data: bytes):
#     with open(f"/app/data/{filename}", "wb") as f:
#         f.write(data)


# @nats_router.subscriber("storage", obj_watch=ObjWatch(declare=False), deliver_policy="new")
# async def file_handler(
#     filename: str,
# ):
#     broker = nats_router.broker
#     object_storage: ObjectStorage = await broker.object_storage("storage")
#     file = await object_storage.get(filename)
#     print(await object_storage.list())

#     # await asyncio.to_thread(write_file, filename, file.data)
#     await object_storage.delete(filename)
