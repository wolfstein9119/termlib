from aiotg import Chat

from ..chat_info import (
    new_chat_info,
    ChatModes,
)
from ..helpers import format_start_message
from ..constants import TG_PARSE_MODE


async def start(chat: Chat, match):
    chat_info = await new_chat_info(
        chat_id=chat.id,
        bot_context=chat.bot.bot_context
    )
    await chat_info.save_to_redis()
    start_message = format_start_message(
        mode_verbose_name=ChatModes.VERBOSE_NAME_RESOLVER[chat_info.mode]
    )
    return chat.reply(
        text=start_message,
        parse_mode=TG_PARSE_MODE
    )
