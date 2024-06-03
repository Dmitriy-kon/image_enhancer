import asyncio

from faststream import Depends, FastStream
from faststream.nats import JStream, NatsBroker, ObjWatch
from faststream.nats.annotations import ObjectStorage

# nats_router = NatsRouter("nats://nats:4222")
# broker = nats_router.broker
broker = NatsBroker("nats://nats:4222")
app = FastStream(broker)


@broker.subscriber(stream="stream", subject="texter", deliver_policy="new")
async def put_text(text: str):
    print(f"{text}, from broker")


def write_file(filename: str, data: bytes):
    with open(f"/app/data/{filename}", "wb") as f:
        f.write(data)


@broker.subscriber("storage", obj_watch=True, deliver_policy="new")
async def file_handler(filename: str):
    print(filename)
    object_storage: ObjectStorage = await broker.object_storage("storage")
    print(await object_storage.list())
    file = await object_storage.get(filename)
    await object_storage.delete(filename)

    # await asyncio.to_thread(write_file, filename, file.data)
    # if data:
    #     print(data.data)
    #     print(data.info)

    # await storage.delete(filename)

    # object_storage: ObjectStorage = await broker.object_storage("storage")
    # file = await object_storage.get(filename)
    # # print(await storage.list())

    # await asyncio.to_thread(write_file, filename, file.data)
    # await object_storage.delete(filename)


@app.after_startup
async def after_startup():
    await broker.object_storage("storage")
