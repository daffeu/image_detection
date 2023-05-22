def create_start_out_message(message):
    task_links = message["links"]
    channel_name = "id_" + message["_id"]["$oid"]
    out_message_dict = dict()
    out_message_dict["channel_name"] = channel_name
    out_message_dict["message"] = f"Start extract links: {len(task_links)}"
    return out_message_dict


def create_group_result(group_id, group_name, response):
    group_result = {
        "group_id": group_id,
        "group_name": group_name,
        "group_image": list()
    }

    for item in response.items:
        if item.attachments:
            for attachment in item.attachments:
                if attachment.photo:
                    group_result["group_image"].append(attachment.photo.sizes[-1].url)

    return group_result
