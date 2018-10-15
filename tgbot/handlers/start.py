from aiotg import Chat


async def start(chat: Chat, match):
    return chat.reply('Привет! Если затрудняешься, то набери /help :)')
