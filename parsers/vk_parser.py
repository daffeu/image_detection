import vk_api
import requests

vk_session = vk_api.VkApi(token='')
vk = vk_session.get_api()

group_id = ''
count = 2


def start(response):
    for item in response['items']:
        if 'attachments' in item:
            for attachment in item['attachments']:
                if attachment['type'] == 'photo':
                    photo_url = attachment['photo']['sizes'][-1]['url']

                    with open(f"{attachment['photo']['id']}.jpg", "wb") as photo_file:
                        response = requests.get(photo_url)
                        photo_file.write(response.content)


if __name__ == "__main__":
    response = vk.wall.get(owner_id='-' + group_id, count=count)
    print(response)
    start(response)