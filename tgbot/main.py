import optparse
import asyncio

from aiotg import Bot

from tgbot.config import load_settings
from tgbot.router import set_routes
from tgbot.context import init_all_context


def _get_options():
    parser = optparse.OptionParser()
    parser.add_option(
        '-c', '--config',
        action='store', dest='config', default='config.ini',
        help='config filename'
    )
    options, args = parser.parse_args()
    return options


def main():
    options = _get_options()
    config = load_settings(options.config)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        init_all_context(config=config)
    )

    bot = Bot(
        api_token=config.tg_api_token
    )
    set_routes(
        bot=bot
    )
    bot.run()


if __name__ == '__main__':
    main()
