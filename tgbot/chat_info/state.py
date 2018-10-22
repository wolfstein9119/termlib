import typing
import dataclasses
import pickle

from ..context import BotContext
from .modes import ChatModes


@dataclasses.dataclass
class ChatStateInRedis:
    mode: str


class ChatState:
    def __init__(self, chat_id: int, bot_context: BotContext):
        self._chat_id = chat_id
        self._bot_context = bot_context
        self._set_defaults()

    @property
    def redis(self):
        return self._bot_context.dialog_redis

    @property
    def mode(self):
        return self._mode

    async def load_from_redis(self):
        stored_state = await self._get_from_redis()
        if not stored_state:
            return

        self._update_fields_from_redis(
            stored_state=stored_state
        )

    async def save_to_redis(self) -> bool:
        stored_state = self.serialize_redis()
        if not stored_state:
            return False

        return await self.redis.set(
            key=self._chat_id,
            value=stored_state,
        )

    @staticmethod
    def deserialize_redis(pickled_state: bytes) -> typing.Optional[ChatStateInRedis]:
        try:
            stored_state = pickle.loads(pickled_state)
        except pickle.UnpicklingError as e:
            # TODO: to logger
            return None

        assert isinstance(stored_state, ChatStateInRedis), 'unknown stored state (ChatInfoInRedis)'
        return stored_state

    def serialize_redis(self) -> typing.Optional[bytes]:
        stored_state = ChatStateInRedis(
            mode=self._mode
        )
        try:
            return pickle.dumps(stored_state)
        except pickle.PickleError as e:
            # TODO: to logger
            pass
        return None

    def _set_defaults(self):
        self._mode = ChatModes.DEFAULT_MODE

    async def _get_from_redis(self) -> typing.Optional[ChatStateInRedis]:
        d = await self.redis.get(self._chat_id)
        if not d:
            return None
        return ChatState.deserialize_redis(d)

    def _update_fields_from_redis(self, stored_state: ChatStateInRedis):
        self._mode = stored_state.mode


async def new(chat_id: int, bot_context: BotContext) -> ChatState:
    info = ChatState(
        chat_id=chat_id,
        bot_context=bot_context,
    )
    await info.load_from_redis()
    return info
