from aiotg import Chat

from .bot import Bot

from .handlers import (
    start,
    help,
)


def set_routes(bot: Bot):
    @bot.command(r'/start')
    async def start_handler(chat: Chat, match):
        await start(chat, match)

    @bot.command(r'/help')
    async def help_handler(chat: Chat, match):
        await help(chat, match)

    @bot.default
    async def echo(chat: Chat, message):
        return chat.reply(message['text'])
