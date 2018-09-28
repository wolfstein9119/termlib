import os
import collections


_PostgresConnectionParams = collections.namedtuple(
    '_PostgresConnectionParams',
    (
        'host',
        'port',
        'user',
        'password',
        'database'
    )
)


class PostgresConnectionParams(_PostgresConnectionParams):
    @property
    def dsn(self) -> str:
        return 'postgres://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'.format(
            PG_USER=self.user,
            PG_PASSWORD=self.password,
            PG_HOST=self.host,
            PG_PORT=self.port,
            PG_DATABASE=self.database,
        )


def get_postgres_connection_params(prefix: str='POSTGRES') -> PostgresConnectionParams:
    _PG_PASSWORD = os.environ.get(f'{prefix}_PASSWORD')
    assert _PG_PASSWORD, 'PG_PASSWORD is empty!'

    return PostgresConnectionParams(
        host=os.environ.get(f'{prefix}_HOST') or '127.0.0.1',
        port=os.environ.get(f'{prefix}_PORT') or 5432,
        user=os.environ.get(f'{prefix}_USER') or 'termlib',
        password=_PG_PASSWORD,
        database=os.environ.get(f'{prefix}_DB') or 'termlib'
    )
