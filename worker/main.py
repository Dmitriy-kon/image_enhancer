import asyncio

from faststream import Depends, FastStream
from faststream.nats import JStream, NatsBroker, ObjWatch
from faststream.nats.annotations import ObjectStorage
from nats.js.errors import BucketNotFoundError

broker = NatsBroker("nats://nats:4222")
app = FastStream(broker)


@broker.subscriber(stream="stream", subject="texter", deliver_policy="new")
async def put_text(text: str):
    print(f"{text}, from broker")


def write_file(filename: str, data: bytes):
    with open(f"/app/data/{filename}", "wb") as f:
        f.write(data)


@broker.subscriber("storage", obj_watch=ObjWatch(declare=False))
async def file_handler(filename: str, object_storage: ObjectStorage):
    print(filename)
    file = await object_storage.get(filename)
    print([i.name for i in await object_storage.list()])
    await object_storage.delete(filename)

    await asyncio.to_thread(write_file, filename, file.data)


# @app.after_startup
# async def after_startup():
#     try:
#         object_store = await broker.object_storage("storage")
#     except BucketNotFoundError:
#         object_store = await broker.object_storage("storage")
