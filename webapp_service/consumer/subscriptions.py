import aiormq

from consumer import methods
from secutiry.settings import AMQP_URI
from secutiry.settings import AMQP_PORT
from secutiry.settings import UNIQUE_PREFIX


async def consumer_subscriptions():
    while True:
        try:
            connection = await aiormq.connect(f"amqp://user:password@{AMQP_URI}:{AMQP_PORT}")
            print('Success!')
            break
        except:
            print('Wait')
            continue
    channel = await connection.channel()
    chat_message_queue__declared = await channel.queue_declare(f"{UNIQUE_PREFIX}:"
                                                               f"external__main:vk_extractor_message",
                                                               durable=False)
    await channel.basic_consume(chat_message_queue__declared.queue, methods.chat_message, no_ack=False)
