import logging
import requests
from .cache import Cache

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# def set_logger(_logger):
#     global logger
#     logger = _logger


class WebPage:
    def __init__(self, url, enable_cache=False, filename="webpage.html"):
        # logger.debug(f"{__class__.__name__}: init(url={url}, enable_cache={enable_cache}, filename={filename})")
        logger.debug(f"{__class__.__name__}: init(url={url}, enable_cache={enable_cache}, filename={filename})")
        self.url = url
        # self.enable_cache = enable_cache
        self.cache = Cache(filename, enable_cache)
        self.filename = filename
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                          "Version/14.0.2 Safari/605.1.15",
            "Accept-Language": "en-US"
        }
        self.response: requests.Response = None
        self.webpage: str = ""

    def set_header(self, key, value):
        logger.debug(f"{__class__.__name__}: setting header: {key}={value}")
        self.headers.update({key: value})

    def set_headers(self, headers: dict):
        logger.debug(f"{__class__.__name__}: setting headers: {headers}")
        self.headers = headers

    def download(self) -> str:
        #
        #   get webpage as text
        #
        logger.debug(f"{__class__.__name__}: downloading {self.url}...")
        self.response = requests.get(self.url, headers=self.headers)
        self.webpage = self.response.text
        return self.webpage

    def get(self, update=False):
        logger.debug(f"{__class__.__name__}: getting page")
        if self.cache.is_enabled():
            if self.cache.is_cached():
                self.webpage = self.cache.get(update, self.download())
            else:
                self.webpage = self.download()
                self.cache.update(self.webpage)
        else:
            self.webpage = self.download()

        return self.webpage
