import optparse
import asyncio

from tgbot.bot import Bot
from tgbot.config import load_settings
from tgbot.router import set_routes
from tgbot.context import get_bot_context


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
    bot_context = loop.run_until_complete(
        get_bot_context(config=config)
    )

    bot = Bot(
        bot_context=bot_context,
        api_token=config.tg_api_token
    )
    set_routes(
        bot=bot
    )
    bot.run()


if __name__ == '__main__':
    main()
