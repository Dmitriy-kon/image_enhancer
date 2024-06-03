import asyncio

import nats
from nats.js.api import ObjectMeta
from nats.js.errors import BucketNotFoundError


servers = "nats://nats:4222"
bucket_name = "configs"


async def main():
    nc = await nats.connect(servers=servers)

    js = nc.jetstream()

    try:
        object_store = await js.object_store(bucket_name)
    except BucketNotFoundError:
        object_store = await js.create_object_store(bucket_name)

    entries = await object_store.list()

    await nc.close()


if __name__ == "__main__":
    asyncio.run(main())
