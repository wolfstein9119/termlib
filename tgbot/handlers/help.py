from aiotg import Chat


async def help(chat: Chat, match):
    return chat.reply('Все будет хорошо :)')
