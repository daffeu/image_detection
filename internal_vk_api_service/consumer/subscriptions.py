import aiormq

from consumer import methods
from settings import AMQP_URI
from settings import AMQP_PORT
from settings import UNIQUE_PREFIX


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

    task_message_queue__declared = await channel.queue_declare(f"{UNIQUE_PREFIX}:"
                                                               f"internal__messager:vk_extractor",
                                                               durable=False)

    await channel.basic_consume(task_message_queue__declared.queue,
                                methods.get_task_data,
                                no_ack=False)
