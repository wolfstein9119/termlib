from ..constants import START_MESSAGE_TEMPLATE


def format_start_message(mode_verbose_name: str) -> str:
    return START_MESSAGE_TEMPLATE.format(
        mode_verbose_name=mode_verbose_name
    )
