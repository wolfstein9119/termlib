from .redis import (
    init_redis_connections,
    dialog_redis_pool,
)
from ..config import TgBotSettings


async def init_all_context(config: TgBotSettings):
    await init_redis_connections(config)
