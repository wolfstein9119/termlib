from typing import Optional

import aioredis


class ChatMode:
    TERMS = 0

    AVAILABLE_MODE = (
        TERMS,
    )

    DEFAULT_MODE = TERMS


class ChatInfo:
    def __init__(self, chat_id: int):
        self._chat_id = chat_id

    async def _load_from_redis(self):
        pass

    def _set_defaults(self):
        self._mode = ChatMode.DEFAULT_MODE


async def new(chat_id: int) -> ChatInfo:
    info = ChatInfo(
        chat_id=chat_id
    )
    return info
