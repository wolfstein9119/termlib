import os

from aiotg import Bot

API_TOKEN = os.environ.get('TG_API_TOKEN')
assert API_TOKEN, 'environment variable TG_API_TOKEN must not be empty'

bot = Bot(api_token=API_TOKEN)


@bot.default
def echo(chat, message):
    return chat.reply(message["text"])


bot.run()
