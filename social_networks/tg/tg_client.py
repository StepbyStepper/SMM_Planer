from telegram import Bot
from telegram.error import TelegramError

from config import TG_BOT_TOKEN


bot = Bot(token=TG_BOT_TOKEN)


def tg_send_message(chat_id, text: str):
    try:
        return bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode="HTML"
        )
    except TelegramError as e:
        raise e


def tg_send_photo(chat_id, photo: str, caption: str | None = None):
    try:
        return bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
            parse_mode="HTML"
        )
    except TelegramError as e:
        raise e


def tg_send_animation(chat_id, animation: str, caption: str | None = None):
    try:
        return bot.send_animation(
            chat_id=chat_id,
            animation=animation,
            caption=caption,
            parse_mode="HTML"
        )
    except TelegramError as e:
        raise e
