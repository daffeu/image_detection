import aiormq
import json
from settings import UNIQUE_PREFIX
from settings import AMQP_URI


async def send_message_to_external_main(out_message):
    print(f"AMQP PRODUCER:     send_message_to_external_main")
    out_message_bytes = json.dumps(out_message).encode()
    connection = await aiormq.connect(AMQP_URI)
    channel = await connection.channel()
    await channel.basic_publish(out_message_bytes, routing_key=f"{UNIQUE_PREFIX}:"
                                                               f"external__main:vk_extractor_message")
    await connection.close()
