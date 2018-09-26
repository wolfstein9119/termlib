import asyncio
from concurrent.futures import (
    ProcessPoolExecutor,
    ThreadPoolExecutor,
)

import asyncpg

from eupdater import get_update_handlers
from helpers import (
    get_postgres_connection_params,
    ElasticContext,
)


async def main():
    postgres_connection_param = get_postgres_connection_params()

    with ProcessPoolExecutor() as process_pool:
        with ThreadPoolExecutor() as thread_pool:
            pg_conn = await asyncpg.connect(dsn=postgres_connection_param.dsn)
            try:
                async with ElasticContext() as elastic_context:
                    update_handlers = get_update_handlers(
                        pg_conn=pg_conn,
                        elastic_context=elastic_context,
                        thread_pool=thread_pool,
                        process_pool=process_pool
                    )
                    # TODO: тут можно добавить функцию выбора обновляторов, в зависимости от режимов работу
                    update_tasks = [
                        asyncio.create_task(u())
                        for u in update_handlers.values()
                    ]
                    for task in update_tasks:
                        await task
            finally:
                await pg_conn.close()


asyncio.run(main())
