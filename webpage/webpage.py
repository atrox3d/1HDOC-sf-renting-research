import requests


# this url does not work due to react
# URL = "https://www.empireonline.com/movies/features/best-movies-2/"
# URL = "http://web.archive.org/web/20200322005914/https://www.empireonline.com/movies/features/best-movies-2/"
# INPUT_FILENAME = "movies.html"
# OUTPUT_FILENAME = "movies.txt"

class WebPage:
    def __init__(self, url, cache=False, filename="webpage.html"):
        self.url = url
        self.cache = cache
        self.filename = filename
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                          "Version/14.0.2 Safari/605.1.15",
            "Accept-Language": "en-US"
        }
        self.response: requests.Response = None
        self.webpage: str = ""

    def set_header(self, key, value):
        self.headers.update({key: value})

    def set_headers(self, headers: dict):
        self.headers = headers

    def download(self) -> str:
        #
        #   get webpage as text
        #
        self.response = requests.get(self.url, headers=self.headers)
        self.webpage = self.response.text
        return self.webpage

    def save(self) -> None:
        #
        #   save webpage to file
        #
        with open(self.filename, "w", encoding="utf-8") as fp:
            fp.write(self.webpage)

    def load(self) -> str:
        #
        #   load webpage from file
        #
        with open(self.filename, encoding="utf-8") as fp:
            self.webpage = fp.read()
            return self.webpage

    def get(self, update=False):
        file_exists = False
        try:
            with open(self.filename):
                file_exists = True
        except FileNotFoundError:
            pass

        if self.cache:
            if file_exists:
                if update:
                    print(f"cache update enabled")
                    print(f"downloading {self.url}...")
                    self.webpage = self.download()
                    print(f"saving {self.url} to {self.filename}...")
                    self.save()
                else:
                    print(f"{self.filename} exists")
                    print(f"loading {self.url} from {self.filename}...")
                    self.webpage = self.load()
            else:
                print(f"{self.filename} does not exists")
                print(f"downloading {self.url}...")
                self.webpage = self.download()
                print(f"saving {self.url} to {self.filename}...")
                self.save()
        else:
            print(f"downloading {self.url}...")
            self.webpage = self.download()

        return self.webpage

