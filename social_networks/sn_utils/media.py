import os
import requests
from urllib.parse import urlparse


def detect_media_type(url: str) -> str | None:
    """
    Возвращает:
    - "image"
    - "gif"
    - None
    """

    # 1️⃣ пробуем по расширению
    path = urlparse(url).path
    extension = os.path.splitext(path)[1].lower()

    if extension == ".gif":
        return "gif"

    if extension in {".jpg", ".jpeg", ".png", ".webp"}:
        return "image"

    # 2️⃣ если расширения нет — проверяем headers
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        content_type = response.headers.get("Content-Type", "")

        if "gif" in content_type:
            return "gif"

        if "image" in content_type:
            return "image"

    except Exception:
        pass

    return None
