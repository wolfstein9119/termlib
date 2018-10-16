import pickle

from .context import BotContext


class ChatMode:
    TERMS = 1

    AVAILABLE_MODE = (
        TERMS,
    )

    DEFAULT_MODE = TERMS


class ChatInfo:
    def __init__(self, chat_id: int, bot_context: BotContext):
        self.__chat_id = chat_id
        self.__bot_context = bot_context
        self._set_defaults()

    async def load_from_redis(self):
        redis = self.__bot_context.dialog_redis
        d = await redis.get(self.__chat_id)
        if d:
            pass
        else:
            pass

    def _set_defaults(self):
        self._mode = ChatMode.DEFAULT_MODE

    def _save_to_redis(self):
        pass

    def _redis_serialize(self):
        pass


async def new(chat_id: int, bot_context: BotContext) -> ChatInfo:
    info = ChatInfo(
        chat_id=chat_id,
        bot_context=bot_context,
    )
    await info.load_from_redis()
    return info
