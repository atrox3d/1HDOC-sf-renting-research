import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Record:
    def __init__(self, address, link, price):
        self.address = address
        self.link = link
        self.price = price
