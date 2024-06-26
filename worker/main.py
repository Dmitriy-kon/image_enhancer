import asyncio

from adapters.s3.s3 import S3Client
from config import config
from faststream import Depends, FastStream
from faststream.nats import JStream, NatsBroker, ObjWatch
from faststream.nats.annotations import ObjectStorage
from servicies.image_service import ImageService

broker = NatsBroker(config.nats_config.broker_url)
app = FastStream(broker)


@broker.subscriber(stream="stream", subject="texter", deliver_policy="new")
async def put_text(text: str):
    print(f"{text}, from broker")


@broker.subscriber(config.nats_config.bucket_name, obj_watch=ObjWatch(declare=False))
async def file_handler(filename: str, object_storage: ObjectStorage):
    image_service = ImageService(object_storage)
    image = await image_service.get_image(filename)

    print([i.name for i in await object_storage.list()])
    image = image_service.process_image(image)
    await image_service.put_image(image)

    # file = await object_storage.get(filename)
    # headers = file.info.headers

    # print(headers)

    # await s3_storage_inner.upload_file(filename, file.data)

    # await object_storage.delete(filename)

    # await asyncio.to_thread(write_file, filename, file.data)


# @app.after_startup
# async def after_startup():
#     await s3_storage_inner.create_bucket_if_not_exists()


#     try:
#         object_store = await broker.object_storage("storage")
#     except BucketNotFoundError:
#         object_store = await broker.object_storage("storage")
