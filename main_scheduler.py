from app.services.sheets_service import SheetsService
from social_networks.publish import publish_post
from social_networks.delete import delete_post
from app.app_utils.datetime_utils import is_time_to_publish
from utils.tipograph import format_text
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz


def process_posts():
    sheets = SheetsService()
    posts = sheets.get_all_posts()

    for idx, post in enumerate(posts, start=2):  # start=2 учитывает заголовки
        try:
            # --- Публикация ---
            if post.get("tg") == "TRUE" and not post.get("status"):
                if is_time_to_publish(post["publish_at"]):
                    sheets.update_status(idx, "processing")

                    result = publish_post(
                        format_text(post["text"]),
                        media_url=post.get("media_url"),
                        telegram=True,
                        vk=post.get("vk") == "TRUE",
                        ok=post.get("ok") == "TRUE"
                    )

                    # Сохраняем message_id в колонку I
                    if result['telegram']['success']:
                        sheets.update_cell(
                            idx, 'I', result['telegram']['message_id'])

                    sheets.update_status(idx, "Опубликовано")
                    print(f"✅ Опубликовано: {post['text']} | {result}")

            # --- Удаление ---
            delete_at = post.get("delete_at")
            if delete_at:
                for fmt in ("%d.%m.%Y %H:%M:%S", "%d.%m.%Y %H:%M"):
                    try:
                        delete_time = datetime.strptime(delete_at, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    raise ValueError(
                        f"Невозможно распарсить дату удаления: {delete_at}")

                if datetime.now() >= delete_time:
                    # Используем message_id для точного удаления
                    message_id = post.get("telegram_message_id")
                    if message_id:
                        delete_post(message_id, telegram=True)
                        sheets.update_status(idx, "Удален")
                        print(
                            f"🗑 Удалено: пост {idx} (Telegram ID: {message_id})")
                    else:
                        print(
                            f"⚠️ Нет message_id для поста {idx}, удалить не удалось")

        except Exception as e:
            sheets.update_status(idx, "Ошибка")
            print(f"❌ Ошибка поста {idx}: {e}")


if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone=pytz.timezone("Asia/Almaty"))
    scheduler.add_job(process_posts, 'interval', seconds=30)
    print("🕒 Автопубликация с message_id запущена...")
    scheduler.start()
