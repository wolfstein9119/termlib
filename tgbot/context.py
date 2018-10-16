import collections

import aioredis

from .config import TgBotSettings


BotContext = collections.namedtuple(
    'BotContext',
    (
        'dialog_redis',
    )
)


async def _get_redis_dialog(config: TgBotSettings) -> aioredis.ConnectionsPool:
    redis_pool = await aioredis.create_redis_pool(
        config.redis_dialog_dsn
    )
    return redis_pool


async def get_bot_context(config: TgBotSettings) -> BotContext:
    return BotContext(
        dialog_redis=await _get_redis_dialog(config)
    )
