import bs4
from bs4 import BeautifulSoup
import logging
from pprint import pprint

import webpage
import util.logger

# import os
# print(os.getcwd(), __name__, __package__)

#
#   fix relative import
#
if __name__ == "__main__":
    #
    #   absolute import
    #
    from record import Record
else:
    #
    #   relative import
    #
    from .record import Record

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# logger = util.logger.get_cli_logger(__name__)
# webpage.set_logger(logger.getChild("webpage"))
# webpage.logger.name = "__main__.carlo"

class Zillow:
    def __init__(self, url):
        logger.debug(f"{__class__.__name__}: init(url={url})")
        self.url = url
        self.webpage = webpage.WebPage(self.url, enable_cache=True, filename="../zillow.html")
        self.html = self.webpage.get_html(update=False)
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.records = []

    def scrape(self):
        logger.debug(f"{__class__.__name__}: scraping")
        self.records = []
        cards = self.soup.select("div.list-card-info")
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

            current_record = Record(address=address, price=price, link=href)
            self.records.append(current_record)

        return self.records


if __name__ == "__main__":

    URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
          "%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122" \
          ".30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22" \
          "%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D" \
          "%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22" \
          "%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B" \
          "%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price" \
          "%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom" \
          "%22%3A12%7D "

    root = util.logger.get_cli_logger()  # add handler with level DEBUG as opposed to lastresort WARNING

    zillow = Zillow(URL)
    records = zillow.scrape()
    # pprint.pprint(zillow.records, indent=4)
    for record in records:
        print(record.address)
        print(record.price)
        print(record.link)
