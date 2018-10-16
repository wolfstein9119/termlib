from aiotg import Chat

from ..chat_info import new as new_chat_info


async def start(chat: Chat, match):
    chat_info = await new_chat_info(
        chat_id=chat.id,
        bot_context=chat.bot.bot_context
    )
    return chat.reply('Привет! Если затрудняешься, то набери /help :)')
