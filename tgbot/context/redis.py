import contextvars

import aioredis

from ..config import TgBotSettings


dialog_redis_pool = contextvars.ContextVar(
    'dialog_redis_pool', default=None
)


async def init_redis_connections(config: TgBotSettings):
    redis_pool = await aioredis.create_redis_pool(
        config.redis_dialog_dsn
    )
    dialog_redis_pool.set(redis_pool)
