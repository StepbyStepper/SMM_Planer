import re

def format_text(text: str) -> str:
    # Удаляем лишние пробелы
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s([,.!?;:])', r'\1', text)

    # Заменяем кавычки на «ёлочки»
    quote_open = True
    result = ""

    for char in text:
        if char == '"':
            if quote_open:
                result += "«"
            else:
                result += "»"
            quote_open = not quote_open
        else:
            result += char

    text = result

    # Заменяем дефис на тире (только если вокруг пробелы)
    text = re.sub('\s-\s', ' — ', text)

    return text