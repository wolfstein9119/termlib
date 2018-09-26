from typing import Dict
from concurrent.futures import (
    ProcessPoolExecutor,
    ThreadPoolExecutor,
)

from asyncpg.connection import Connection as PgConnection

from helpers import ElasticContext
from .base import BaseUpdater
from .terms import TermUpdater


def get_update_handlers(pg_conn: PgConnection,
                        elastic_context: ElasticContext,
                        thread_pool: ThreadPoolExecutor,
                        process_pool: ProcessPoolExecutor) -> Dict[str, BaseUpdater]:
    """
    Получить резолвер всех обработчиков-обновляторов.

    :param pg_conn:         соединение с СУБД
    :param elastic_context: контекст Эластика
    :param thread_pool:     потоковый пул для асинхронных операций
    :param process_pool:    процессный пул для асинхронных операций
    :return:                резолвер обработчиков-обновляторов
    """
    params = {
        'pg_conn': pg_conn,
        'elastic_context': elastic_context,
        'thread_pool': thread_pool,
        'process_pool': process_pool,
    }

    return {
        'terms': TermUpdater(**params)
    }
