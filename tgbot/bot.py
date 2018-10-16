import aiotg

from .context import BotContext


class Bot(aiotg.Bot):
    def __init__(self, bot_context: BotContext, *args, **kwargs):
        self.__bot_context = bot_context
        super().__init__(*args, **kwargs)

    @property
    def bot_context(self):
        return self.__bot_context
