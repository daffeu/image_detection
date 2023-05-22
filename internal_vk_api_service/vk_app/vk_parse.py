import asyncio
from vkbottle import API
from utils import create_group_result
from settings import VK_TOKEN


async def get_photo_with_vk_links(payload):
    api = API(VK_TOKEN)
    result = {
        "result": list()
    }
    for group in payload["links"]:
        _, g_id = group.split("vk.com/")
        group_info = await api.groups.get_by_id(group_id=g_id)
        group_id, group_name = '-' + str(group_info[0].id), group_info[0].name
        response = await api.wall.get(owner_id=group_id, count=100)
        group_result = create_group_result(group_id=group_id,
                                           group_name=group_name,
                                           response=response)
        result["result"].append(group_result)
    return result


if __name__ == "__main__":
    from loguru import logger
    logger.disable("vkbottle")
    test_payload = {"links": ["https://vk.com/lentach"]}
    asyncio.run(main=get_photo_with_vk_links(test_payload))
