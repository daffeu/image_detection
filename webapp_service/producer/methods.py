import aiormq
import json
from bson import json_util
from secutiry.settings import UNIQUE_PREFIX
from secutiry.settings import AMQP_URI
from models.utils import json_serialize_date


async def send_message_to_vk_extractor(out_message):
    out_message_bytes = json.dumps(out_message, default=json_serialize_date).encode()
    connection = await aiormq.connect(AMQP_URI)
    channel = await connection.channel()
    await channel.basic_publish(out_message_bytes,
                                routing_key=f"{UNIQUE_PREFIX}:internal__messager:vk_extractor")
    await connection.close()
