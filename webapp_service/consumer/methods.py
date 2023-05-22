import json
from channel_box import channel_box


async def chat_message(message):
    incoming_message_dict = json.loads(message.body.decode())
    await channel_box.channel_send(incoming_message_dict["channel_name"],
                                   {"message": f'{incoming_message_dict["message"]}'})
    await message.channel.basic_ack(message.delivery.delivery_tag)
