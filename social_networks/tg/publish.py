from social_networks.tg.tg_publisher import publish_to_telegram
# from social_networks.vk.publisher import publish_to_vk
# from social_networks.ok.publisher import publish_to_ok
from social_networks.sn_utils.media import detect_media_type


def publish_post(
    text: str | None = None,
    media_url: str | None = None,
    telegram: bool = True,
    vk: bool = False,
    ok: bool = False
):
    """
    Универсальная публикация.
    Можно передать:
    - только text
    - только media_url
    - и то и другое
    """

    if not text and not media_url:
        return {"success": False, "error": "Нечего публиковать"}

    results = {}

    image_url = None
    gif_url = None

    # 🔍 автоматически определяем тип
    if media_url:
        media_type = detect_media_type(media_url)

        if media_type == "gif":
            gif_url = media_url
        elif media_type == "image":
            image_url = media_url

    if text is None:
        text = ""

    if telegram:
        results["telegram"] = publish_to_telegram(
            text=text,
            image_url=image_url,
            gif_url=gif_url
        )

    # if vk:
    #     results["vk"] = publish_to_vk(
    #         text=text,
    #         image_url=image_url,
    #         gif_url=gif_url
    #     )

    # if ok:
    #     results["ok"] = publish_to_ok(
    #         text=text,
    #         image_url=image_url,
    #         gif_url=gif_url
    #     )

    return results
