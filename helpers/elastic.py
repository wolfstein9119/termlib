import os
import collections

import elasticsearch_dsl.connections as elastic_dsl_connections


_ElasticConnectionParams = collections.namedtuple(
    '_ElasticConnectionParams',
    (
        'host',
        'port',
    )
)


class ElasticConnectionParams(_ElasticConnectionParams):
    def to_dict(self):
        return {
            'host': self.host,
            'port': self.port,
        }


def get_elasticsearch_connection_params(prefix: str='ELASTICSEARCH') -> ElasticConnectionParams:
    _ELASTICSEARCH_HOST = os.environ.get(f'{prefix}_HOST') or '127.0.0.1'
    _ELASTICSEARCH_PORT = os.environ.get(f'{prefix}_PORT') or 9200

    return ElasticConnectionParams(
        host=_ELASTICSEARCH_HOST,
        port=_ELASTICSEARCH_PORT,
    )


class ElasticContext:
    def __init__(self, connection_alias: str='default', params_prefix: str='ELASTICSEARCH'):
        self._conn_alias = connection_alias
        self._params_prefix = params_prefix

    async def __aenter__(self):
        connection_params = get_elasticsearch_connection_params(
            prefix=self._params_prefix
        )
        conf = {
            self._conn_alias: {
                'hosts': [f'{connection_params.host}:{connection_params.port}']
            }
        }
        elastic_dsl_connections.configure(**conf)
        elastic_dsl_connections.get_connection(self._conn_alias)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        elastic_dsl_connections.remove_connection(self._conn_alias)

    @property
    def current_connection(self):
        return elastic_dsl_connections.get_connection(
            alias=self._conn_alias
        )
