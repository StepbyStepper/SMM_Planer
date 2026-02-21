from social_networks.tg.tg_publisher import delete_from_telegram


def delete_post(
    message_id: int,
    telegram: bool = True,
):
    results = {}

    if telegram:
        results["telegram"] = delete_from_telegram(message_id)

    return results
