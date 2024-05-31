from typing import Annotated
from uuid import uuid4

from color_formatter import color_f
from faststream import Context, FastStream
from faststream.rabbit import (
    ExchangeType,
    RabbitBroker,
    RabbitExchange,
    RabbitMessage,
    RabbitQueue,
)

broker = RabbitBroker("amqp://rabbit")

app = FastStream(broker)

exch = RabbitExchange("test_exchange", type=ExchangeType.DIRECT, auto_delete=True)

queue_1 = RabbitQueue("test", auto_delete=True)
queue_2 = RabbitQueue("another_queue", auto_delete=True)

CorrelationId = Annotated[str, Context("message.correlation_id")]


# @broker.publisher(queue_2, exchange=exch)
@broker.subscriber(queue_1, exchange=exch)
@broker.publisher(queue_2, exchange=exch)
async def base_handler(
    # msg: RabbitMessage,
    name: str,
    user_id: int,
    cor_id: str = Context("message.correlation_id"),
):
    # print(color_f.colorize_blue(f"[ ] worker message gain with id: {cor_id}"))

    # print(
    #     color_f.colorize_green(
    #         f"[ ]Hello {name}, from worker with id {user_id} and your cor_id is {cor_id}"
    #     )
    # )
    return name


# @app.after_startup
# async def test():
#     data = {"name": "Dime", "user_id": 212}
#     _id = uuid4().hex
#     print(color_f.colorize_green(f"[ ] main_app message publish with id: {id}"))
#     await broker.publish(data, exchange=exch, queue=queue_1, correlation_id=_id)
