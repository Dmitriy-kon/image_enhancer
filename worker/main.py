import asyncio

from faststream import Depends, FastStream
from faststream.nats import JStream, NatsBroker, ObjWatch
from faststream.nats.annotations import ObjectStorage
from s3.s3 import S3Client

broker = NatsBroker("nats://nats:4222")
app = FastStream(broker)


s3_storage_inner = S3Client(
    access_key="minioadmin",
    secret_key="minioadmin",
    endpoint_url="http://minio:9000",
    bucket_name="storage",
)
s3_storage_out = S3Client(
    access_key="minioadmin",
    secret_key="minioadmin",
    endpoint_url="http://localhost:9000",
    bucket_name="storage",
)


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

    await s3_storage_inner.upload_file(filename, file.data)
    # await object_storage.delete(filename)

    # await asyncio.to_thread(write_file, filename, file.data)


@app.after_startup
async def after_startup():
    await s3_storage_inner.create_bucket_if_not_exists()


#     try:
#         object_store = await broker.object_storage("storage")
#     except BucketNotFoundError:
#         object_store = await broker.object_storage("storage")
