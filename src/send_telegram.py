import json
import httpx
import re
import os
from dotenv import load_dotenv


load_dotenv()

warning = '⚠️'
success = '✅'
error = '❌'


def escape_markdown(text: str, entity_type: str = None) -> str:
    """
    Helper function to escape telegram markup symbols.
    Args:
        text (:obj:`str`): The text.
        version (:obj:`int` | :obj:`str`): Use to specify the version of telegrams Markdown.
            Either ``1`` or ``2``. Defaults to ``1``.
        entity_type (:obj:`str`, optional): For the entity types ``PRE``, ``CODE`` and the link
            part of ``TEXT_LINKS``, only certain characters need to be escaped in ``MarkdownV2``.
            See the official API documentation for details. Only valid in combination with
            ``version=2``, will be ignored else.
    """
    if entity_type in {'pre', 'code'}:
        escape_chars = r'\`'
    elif entity_type == 'text_link':
        escape_chars = r'\)'
    else:
        escape_chars = r'_*[]()~`>#+-=|{}.!'

    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)


def send_telegram(message):

    data = {
        "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
        "text": escape_markdown(message),
        "parse_mode": "MarkdownV2"
    }
    headers = {
        "Content-Type": "application/json"
    }
    httpx.post("https://api.telegram.org/" + os.getenv("TELEGRAM_BOT_TOKEN") + "/sendMessage",
               data=json.dumps(data), headers=headers)


def t_error(message):
    send_telegram(f'{error} {message}')


def t_success(message):
    send_telegram(f'{success} {message}')


def t_warning(message):
    send_telegram(f'{warning} {message}')


def send_message(message):
    send_telegram(message)
