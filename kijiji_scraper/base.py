import re
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

from .utils import parse_table


HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/31.0.1650.57 "
                         "Safari/537.36"}
BASE_URL = "http://www.kijiji.ca"
DATE_FIELD_NAME = "Date de l'affichage"
PRICE_FIELD_NAME = 'Prix'
ADDRESS_FIELD_NAME = 'Adresse'
BATHROOMS_FIELD_NAME = 'Salles de bain (nb)'
RENT_BY_FIELD_NAME = 'À louer par'
FURNISHED_FIELD_NAME = 'Meublé'
ANIMALS_FIELD_NAME = 'Animaux acceptés'


class KPage(object):
    def __init__(self, url):
        self.url = url
        self.text = requests.get(self.url, headers=HEADERS).text
        self.soup = BeautifulSoup(self.text, 'html.parser')


class Item(KPage):
    """One kijiji ad."""
    def __init__(self, link):
        super(Item, self).__init__(link)

    @property
    def attr_table(self):
        if not hasattr(self, '_attr_table'):
            raw_table = self.soup.find(class_='ad-attributes')
            parsed_table = parse_table(raw_table)
            self._attr_table = OrderedDict(
                line for line in parsed_table if line)
        return self._attr_table

    @property
    def description(self):
        if not hasattr(self, '_description'):
            self._description = self.soup.find(id="UserContent").text
        return self._description

    @property
    def date(self):
        return self.attr_table[DATE_FIELD_NAME]

    @property
    def price(self):
        raw_price = self.attr_table[PRICE_FIELD_NAME]
        raw_price = re.sub('[^\d.,]', '', raw_price)
        raw_price = re.sub(',', '.', raw_price)
        return float(raw_price)

    @property
    def address(self):
        return self.attr_table[ADDRESS_FIELD_NAME].split('\n')[0]

    @property
    def bathrooms(self):
        return self.attr_table[BATHROOMS_FIELD_NAME]

    @property
    def rent_by(self):
        return self.attr_table[RENT_BY_FIELD_NAME]

    @property
    def furnished(self):
        return self.attr_table[FURNISHED_FIELD_NAME]

    @property
    def animals(self):
        return self.attr_table[ANIMALS_FIELD_NAME]


class List(KPage):
    """List of kijiji ads."""
    def __init__(self, url):
        super(List, self).__init__(url)

    @property
    def list(self):
        if not hasattr(self, '_list'):
            self._list = []
            for item in self.soup.find_all(class_='search-item top-feature '):
                addr = item.attrs['data-vip-url']
                self._list.append(Item(BASE_URL + addr))

        return self._list

    def __iter__(self):
        return iter(self.list)
