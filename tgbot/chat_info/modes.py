import collections


class ChatModes:
    TERMS = 1

    AVAILABLE_MODE = (
        TERMS,
    )

    DEFAULT_MODE = TERMS

    VERBOSE_NAME_RESOLVER = collections.OrderedDict([
        (TERMS, 'Термины и понятия'),
    ])
