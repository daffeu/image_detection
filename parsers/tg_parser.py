from telethon import TelegramClient, events
import asyncio


API_ID = ''
API_HASH = ''
SESSION_NAME = '1'
CHANNEL_USERNAME = ''
PHOTOS_TO_COLLECT = 10


client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


async def start():
    await client.start()
    channel = await client.get_entity(CHANNEL_USERNAME)
    photos = []
    async for message in client.iter_messages(channel, limit=PHOTOS_TO_COLLECT):
        if message.photo:
            photos.append(message.photo)
    for i, photo in enumerate(photos):
        file_name = f'photo_{i}.jpg'
        await client.download_media(photo, file=file_name)
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(start())