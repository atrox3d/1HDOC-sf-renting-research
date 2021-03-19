import bs4
from bs4 import BeautifulSoup
import webpage
import util.logger
import logging
from pprint import pprint

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

root = util.logger.get_cli_logger()  # add handler with level DEBUG as opposed to lastresort WARNING
# logger = util.logger.get_cli_logger(__name__)
# webpage.set_logger(logger.getChild("webpage"))
# webpage.logger.name = "__main__.carlo"

URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
      "%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122" \
      ".30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22" \
      "%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D" \
      "%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22" \
      "%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B" \
      "%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price" \
      "%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom" \
      "%22%3A12%7D "


class Zillow:
    def __init__(self, url):
        self.url = url
        self.webpage: webpage.WebPage = None
        self.soup: BeautifulSoup = None
        self.html = ""
        self.records = []

    def _get_page(self):
        logger.debug("get webpage")
        self.webpage = webpage.WebPage(self.url, enable_cache=True, filename="zillow.html")
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

            record = dict(address=address, price=price, link=href)
            self.records.append(record)


zillow = Zillow(URL)
zillow.scrape()
pprint(zillow.records, indent=4)
