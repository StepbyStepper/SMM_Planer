from datetime import datetime


def is_time_to_publish(publish_at_str):
    """
    Проверяет, пришло ли время публикации
    publish_at_str: строка из Google Sheets (формат "%d.%m.%Y %H:%M" или "%d.%m.%Y %H:%M:%S")
    """
    for fmt in ("%d.%m.%Y %H:%M:%S", "%d.%m.%Y %H:%M"):
        try:
            publish_time = datetime.strptime(publish_at_str, fmt)
            break
        except ValueError:
            continue
    else:
        raise ValueError(
            f"Невозможно распарсить дату публикации: {publish_at_str}")
    return datetime.now() >= publish_time
