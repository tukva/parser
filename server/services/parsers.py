import re
import random
import requests
import logging

from itertools import chain
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class BaseParserType(ABC):
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
    ]

    @classmethod
    def get_page(cls, url):
        headers = {'user-agent': random.choice(cls.USER_AGENTS)}
        try:
            page = requests.get(url, headers=headers).text
        except requests.exceptions.RequestException:
            logging.error(f"Exception during request from {cls}", exc_info=True)
            page = None

        if page:
            return BeautifulSoup(page,"html.parser")
        return None

    @classmethod
    def parse_data(cls, url, tag, attrs, text_from='text', filter_func=None, sep=None, **kwargs):

        page = cls.get_page(url)

        if not page:
            return []

        teams = page.findAll(tag, attrs, **kwargs)

        if text_from == 'text':
            result = list({team.text for team in teams})
        elif isinstance(text_from, str):
            result = [team.get(text_from) for team in teams]
        else:
            return []

        if hasattr(filter_func, '__call__'):
            result = list(filter(filter_func, result))

        if isinstance(sep, str):
            result = list(chain(*[item.strip().split(sep) for item in result]))

        return result

    @classmethod
    @abstractmethod
    def parse_teams(cls, url, tag, attrs):
        return cls.parse_data(url=url, tag=tag, attrs=attrs)


class BWinParserType(BaseParserType):
    @classmethod
    @abstractmethod
    def parse_teams(cls, url, tag, attrs):
        filter_func = lambda item: len(item) > 1
        return cls.parse_data(url=url, tag=tag, attrs=attrs, filter_func=filter_func)


class WilliamParserType(BaseParserType):
    @classmethod
    @abstractmethod
    def parse_teams(cls, url, tag, attrs):
        return cls.parse_data(url=url, tag=tag, sep=' v ', attrs=attrs)


PARSER_TYPES = {
    'base': BaseParserType,
    'Free Super Tips': BaseParserType,
    'bwin': BWinParserType,
    'Betandyou': BaseParserType,
    'William Hill': WilliamParserType,
    'UEFA': BaseParserType,
}
