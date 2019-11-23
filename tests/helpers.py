import os
from typing import *

import requests
from bs4 import BeautifulSoup

import config


def is_valid_message(message: str) -> bool:
    """
    :return: True of substring "RED" not in message else False
    """
    try:
        return 'RED' not in message
    except Exception:
        return False


def get_server_path() -> str:
    """
    :return: Absolute path to the server
    """
    split_path = os.path.normpath(__file__).split(os.sep)
    return os.sep.join(split_path[:split_path.index('tests')])


def get_soup(page_content: str, parser: str = "html.parser") -> BeautifulSoup:
    return BeautifulSoup(page_content, parser)


def get_posts() -> List[Dict[str, str]]:
    """
    :return: list of dictionaries {name: <name>, message: <message>}
    """
    response = requests.get(f'http://{config.HOST_NAME}:{config.PORT}/{config.URL_BOARD}')
    soup = get_soup(response.content)
    all_tags = soup.find_all()
    return [{'name': t.text, 'message': all_tags[idx + 1].text} for idx, t in enumerate(all_tags) if t.name == 'h2']
