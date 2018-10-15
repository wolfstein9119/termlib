import os
import configparser
import collections


_TgBotSettings = collections.namedtuple(
    '_TgBotSettings',
    (
        'tg_api_token',
        'redis_dialog_host',
        'redis_dialog_db',
    )
)


class TgBotSettings(_TgBotSettings):
    @property
    def redis_dialog_dsn(self) -> str:
        return f'redis://{self.redis_dialog_host}/{self.redis_dialog_db}'


def _load_tg_api_token() -> str:
    tg_api_token = os.environ.get('TG_API_TOKEN')
    assert tg_api_token, 'environment variable TG_API_TOKEN must not be empty'
    return tg_api_token


def load_settings(filename: str) -> TgBotSettings:
    config = configparser.ConfigParser()
    config.read(filename)

    return TgBotSettings(
        tg_api_token=_load_tg_api_token(),
        redis_dialog_host=config['REDIS DIALOG']['host'],
        redis_dialog_db=config['REDIS DIALOG']['db']
    )
