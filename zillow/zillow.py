import bs4
from bs4 import BeautifulSoup
import logging
from pprint import pprint

import webpage
import util.logger
from .record import Record

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

root = util.logger.get_cli_logger()  # add handler with level DEBUG as opposed to lastresort WARNING


# logger = util.logger.get_cli_logger(__name__)
# webpage.set_logger(logger.getChild("webpage"))
# webpage.logger.name = "__main__.carlo"

class Zillow:
    def __init__(self, url):
        self.url = url
        self.webpage: webpage.WebPage = None
        self.soup: BeautifulSoup = None
        self.html = ""
        self.records = []

    def _get_page(self):
        logger.debug("get webpage")
        self.webpage = webpage.WebPage(self.url, enable_cache=True, filename="../zillow.html")
        return self.webpage

    def _get_html(self):
        logger.debug("get html")
        self.html = self.webpage.get(update=False)
        return self.html

    def _get_soup(self):
        logger.debug("get soup")
        self.soup = BeautifulSoup(self.html, "html.parser")
        return self.soup

    def scrape(self):
        self._get_page()
        self._get_html()
        self._get_soup()
        cards = self.soup.select("div.list-card-info")
        self.records = []
        card: bs4.Tag
        for card in cards:
            link = card.select_one("a.list-card-link")
            href = link.get('href') if link else "NO LINK"
            prefix = "https://www.zillow.com"
            if not href.startswith(prefix):
                href = prefix + href

            pricediv = card.select_one("div.list-card-price")
            price = pricediv.getText() if pricediv else "NO PRICE"

            addresstag = card.select_one("address.list-card-addr")
            address = addresstag.getText() if addresstag else "NO ADDRESS"

            record = Record(address=address, price=price, link=href)
            self.records.append(record)
