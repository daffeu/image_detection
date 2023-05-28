import json

from producer import methods as producer_methods
from utils import create_start_out_message
from vk_app.vk_parse import get_photo_with_vk_links


async def get_task_data(message):
    incoming_message_dict = json.loads(message.body.decode())
    start_payload = create_start_out_message(incoming_message_dict)
    await producer_methods.send_message_to_external_main(start_payload)
    await message.channel.basic_ack(message.delivery.delivery_tag)
    result = await get_photo_with_vk_links(payload=incoming_message_dict)
    print(result)
    # TODO send image link to face detected service
