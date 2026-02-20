from environs import Env

env = Env()
env.read_env()

TG_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')
TG_CHAT_ID = env.str('TELEGRAM_CHAT_ID')
