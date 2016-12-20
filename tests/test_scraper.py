import re

from kijiji_scraper import Item, List


LINK = ('http://www.kijiji.ca/v-appartement-condo-3-1-2/ville-de-montreal/'
        '3-ndg-near-concordia-available-for-now-with-free-parking/1224821529')
LIST_LINK = ('http://www.kijiji.ca/b-appartement-condo/ville-de-montreal/'
             'page-2/c37l1700281r100.0?price=400__550')


def test_item():
    item = Item(LINK)
    assert item.address == '2056 Avenue Trenholme, Montréal, QC H4B 1X6, Canada'
    assert re.findall("typical apartment shown on photos", item.description)
    assert item.price == 545.
    assert item.url == LINK


def test_list():
    list = List(LIST_LINK)
    for item in list:
        assert item.address
        assert item.description
        assert item.price
        assert item.url
