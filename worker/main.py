import asyncio

import nats
from nats.js.api import ObjectMeta
from nats.js.errors import BucketNotFoundError
from nats.js.object_store import ObjectStore

servers = ["nats://nats:4222"]
bucket_name = "storage"


async def connect_to_nats():
    nc = await nats.connect(servers)
    return nc.jetstream()


async def get_object_storage(js) -> ObjectStore:
    try:
        object_storage = await js.object_store(bucket_name)
    except BucketNotFoundError:
        object_storage = await js.create_object_store(bucket_name)

    return object_storage


def write_file(filename: str, data: bytes):
    with open(f"/app/data/{filename}", "wb") as f:
        f.write(data)


async def main():
    js = await connect_to_nats()
    obj_store = await get_object_storage(js)
    print(await obj_store.status())

    for file in await obj_store.list():
        await asyncio.to_thread(write_file, file.name, await obj_store.get(file.name))
        await obj_store.delete(file.name)


if __name__ == "__main__":
    asyncio.run(main())
