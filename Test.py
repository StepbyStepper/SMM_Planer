from social_networks.publish import publish_post
from utils.tipograph import format_text

result = publish_post(
    format_text(
        text='привет    я приехал в клуб с простым названием-"звездочка"'),
    # media_url="https://mir-s3-cdn-cf.behance.net/project_modules/hd/5eeea355389655.59822ff824b72.gif",
    media_url="https://moya-planeta.ru/upload/images/xl/85/ec/85ec639804ea05eb0d5bf4e6793c540e5951d508.jpg",
    telegram=True,
    vk=False,
    ok=False
)

print(result)
