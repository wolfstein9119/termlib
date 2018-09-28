from typing import Iterable, Callable, List
import asyncio
from concurrent.futures import (
    ProcessPoolExecutor,
    ThreadPoolExecutor,
)

from asyncpg.connection import Connection as PgConnection
from asyncpg import Record as PgRecord

from helpers import ElasticContext


def records_to_dict(db_data: List[PgRecord]) -> List[dict]:
    # asyncpg.Record не пиклятся :( вот такой вот костыль...

    return [
        dict(u) for u in db_data
    ]


class BaseUpdater:
    def __init__(self,
                 pg_conn: PgConnection,
                 elastic_context: ElasticContext,
                 thread_pool: ThreadPoolExecutor,
                 process_pool: ProcessPoolExecutor):
        self._pg_conn = pg_conn
        self._elastic_context = elastic_context
        self._thread_pool = thread_pool
        self._process_pool = process_pool

    async def __call__(self, *args, **kwargs):
        db_data = await self.get_data_from_db()
        elastic_data = await self._process_data_to_elastic_model(db_data)
        return await self.save_to_elastic(elastic_data)

    async def get_data_from_db(self) -> List[PgRecord]:
        """
        Получить данные из БД.

        :return:    Итерируемый объект, содержащий кортежи данных из СУБД для загрузки в Эластик.
        """
        raise NotImplementedError()

    def get_elastic_data_processor(self, db_data: List[dict]) -> Callable:
        """
        Получить функцию для преобразования данных в модели эластика.
        Важно! Функция будет работать внутри self._process_pool.

        :param db_data: Кортежи данных из СУБД
        :return:        Функция для преобразования данных
        """
        raise NotImplementedError()

    async def _process_data_to_elastic_model(self, db_data: List[PgRecord]) -> Iterable:
        """
        Преобразовать данные из кортежей СУБД в модели Эластика.

        :param db_data:     Кортежи данных из СУБД
        :return:            Итерируемые объект, содержащий модели Эластика.
        """
        loop = asyncio.get_running_loop()
        db_data = records_to_dict(db_data)
        elastic_data = await loop.run_in_executor(
            executor=self._process_pool,
            func=self.get_elastic_data_processor(db_data)
        )
        return elastic_data

    def get_elastic_saver(self, elastic_data: Iterable) -> Callable:
        """
        Получить функцию для сохранения данных в Эластик.
        Важно! Функция будет работать внутри self._thread_pool.

        :param elastic_data:    Список моделей для Эластика
        :return:                Функция для сохранения данных
        """
        raise NotImplementedError()

    async def save_to_elastic(self, elastic_data: Iterable) -> bool:
        raise NotImplementedError()
