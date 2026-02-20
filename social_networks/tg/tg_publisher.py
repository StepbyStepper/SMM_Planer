from telegram.error import TelegramError
from .tg_client import tg_send_message, tg_send_photo, tg_send_animation
from config import TG_CHAT_ID


def publish_to_telegram(
    text: str = "",
    image_url: str | None = None,
    gif_url: str | None = None
):
    """
    Универсальная публикация в Telegram.

    Можно передать:
    - только text
    - только image_url
    - только gif_url
    - text + image_url
    - text + gif_url
    """

    try:

        if gif_url:
            message = tg_send_animation(
                chat_id=TG_CHAT_ID,
                animation=gif_url,
                caption=text if text else None
            )

        elif image_url:
            message = tg_send_photo(
                chat_id=TG_CHAT_ID,
                photo=image_url,
                caption=text if text else None
            )
        else:
            message = tg_send_message(
                chat_id=TG_CHAT_ID,
                text=text
            )

        return {
            "success": True,
            "message_id": message.message_id
        }

    except TelegramError as e:
        return {
            "success": False,
            "error": str(e)
        }
