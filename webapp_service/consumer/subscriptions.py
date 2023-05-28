import aiormq

from consumer import methods
from secutiry.settings import AMQP_URI
from secutiry.settings import UNIQUE_PREFIX


async def consumer_subscriptions():
    print(f"AMQP CONSUMER:     ready [yes] PREFIX={UNIQUE_PREFIX}")
    connection = await aiormq.connect(AMQP_URI)
    channel = await connection.channel()
    chat_message_queue__declared = await channel.queue_declare(f"{UNIQUE_PREFIX}:"
                                                               f"external__main:vk_extractor_message",
                                                               durable=False)
    await channel.basic_consume(chat_message_queue__declared.queue, methods.chat_message, no_ack=False)
