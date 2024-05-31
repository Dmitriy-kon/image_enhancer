import asyncio
from typing import Annotated
from uuid import uuid4

from color_formatter import color_f
from faststream import Context, FastStream
from faststream.exceptions import AckMessage, NackMessage, RejectMessage
from faststream.rabbit import (
    ExchangeType,
    RabbitBroker,
    RabbitExchange,
    RabbitQueue,
)
from faststream.rabbit.annotations import RabbitMessage

broker = RabbitBroker("amqp://rabbit")

app = FastStream(broker)

exch = RabbitExchange("test_exchange", auto_delete=True)

queue_1 = RabbitQueue("test", auto_delete=True)
queue_2 = RabbitQueue("another_queue", auto_delete=True)

CorrelationId = Annotated[str, Context("message.correlation_id")]


# @broker.publisher(queue_2, exchange=exch)
# @broker.subscriber(queue_1, exchange=exch)
# async def base_handler(
#     # msg: RabbitMessage,
#     name: str,
#     user_id: int,
#     cor_id: str = Context("message.correlation_id"),
# ):
#     print(color_f.colorize_blue(f"[ ] main_app message gain with id: {id}"))

#     print(
#         f"Hello {name}, from base_handler with id {user_id} and your cor_id is {cor_id}"
#     )


@broker.subscriber(queue_2, exchange=exch, no_ack=True, retry=2)
async def worker_handle2(
    msg: RabbitMessage,
    name: str,
):
    if name == "Dime":
        print(
            color_f.colorize_red(
                f"[ ] main_app:worker_handle2 get message from worker with data: {name}"
            )
        )
        # await msg.reject()
        # raise NackMessage("NackMessage")
        return

    print(
        color_f.colorize_blue(
            f"[ ] main_app:worker_handle2 get message from woeker with data: {name} gain with id: {msg.correlation_id}"
        )
    )
    await msg.ack()


@broker.subscriber(queue_2, exchange=exch, no_ack=True)
async def worker_handle(
    msg: RabbitMessage,
    name: str,
):
    if name != "Dime":
        await msg.nack()
        print(
            color_f.colorize_red(
                f"[ ] main_app:worker_handle1 this must be Dime: but your name is {name}"
            )
        )
        return
        # raise NackMessage("NackMessage")

    print(
        color_f.colorize_blue(
            f"[ ] main_app:worker_handle1 get message from worker with data: {name} gain with id: {msg.correlation_id} Hello DIMA"
        )
    )
    await msg.ack()


@app.after_startup
async def test():
    data = {"name": "Dime", "user_id": 212}
    data2 = {"name": "Artem", "user_id": 212}
    data3 = {"name": "Denis", "user_id": 212}
    _id = uuid4().hex
    _id2 = uuid4().hex
    print(color_f.colorize_green(f"[ ] main_app message publish with id: {_id}"))
    await broker.publish(data, exchange=exch, queue=queue_1, correlation_id=_id)
    await broker.publish(data, exchange=exch, queue=queue_1, correlation_id=_id)
    await broker.publish(data, exchange=exch, queue=queue_1, correlation_id=_id)
    await broker.publish(data, exchange=exch, queue=queue_1, correlation_id=_id)
    await broker.publish(data2, exchange=exch, queue=queue_1, correlation_id=_id2)
    await broker.publish(data2, exchange=exch, queue=queue_1, correlation_id=_id2)
    await broker.publish(data2, exchange=exch, queue=queue_1, correlation_id=_id2)
    await broker.publish(data2, exchange=exch, queue=queue_1, correlation_id=_id2)
    await broker.publish(data3, exchange=exch, queue=queue_1, correlation_id=_id2)
    await broker.publish(data3, exchange=exch, queue=queue_1, correlation_id=_id2)
    await broker.publish(data3, exchange=exch, queue=queue_1, correlation_id=_id2)
    await broker.publish(data3, exchange=exch, queue=queue_1, correlation_id=_id2)
