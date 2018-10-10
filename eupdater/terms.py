from typing import Iterable, Callable, List
from functools import partial
import asyncio

from asyncpg import Record as PgRecord
from elasticsearch.helpers import bulk

from models.elastic import Term
from .base import BaseUpdater


def elastic_data_processor(db_data: List[dict]) -> List[Term]:
    return [
        Term(
            id=u['id'],
            name=u['name'],
            definitions=u['definitions']
        )
        for u in db_data
    ]


def prepare_for_bulk_elastic(elastic_data: List[Term]) -> List[dict]:
    return [
        u.to_dict(include_meta=True) for u in elastic_data
    ]


def save_to_elastic(elastic_conn, elastic_data: List[dict]) -> Iterable:
    return bulk(
        client=elastic_conn,
        actions=elastic_data
    )


class TermUpdater(BaseUpdater):
    async def get_data_from_db(self) -> List[PgRecord]:
        return await self._pg_conn.fetch('SELECT * FROM public.terms_with_definitions')

    def get_elastic_data_processor(self, db_data: List[PgRecord]) -> Callable:
        db_data = [dict(u) for u in db_data]
        return partial(elastic_data_processor, db_data=db_data)

    async def save_to_elastic(self, elastic_data: Iterable) -> bool:
        loop = asyncio.get_running_loop()
        prepared_data = await loop.run_in_executor(
            executor=self._process_pool,
            func=partial(prepare_for_bulk_elastic, elastic_data=elastic_data)
        )
        Term.reinit_index()
        result = await loop.run_in_executor(
            executor=self._thread_pool,
            func=partial(
                save_to_elastic,
                elastic_conn=self._elastic_context.current_connection,
                elastic_data=prepared_data
            )
        )
        return True
