import bs4
from bs4 import BeautifulSoup
import requests

URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"


# this url does not work due to react
# URL = "https://www.empireonline.com/movies/features/best-movies-2/"
# URL = "http://web.archive.org/web/20200322005914/https://www.empireonline.com/movies/features/best-movies-2/"
# INPUT_FILENAME = "movies.html"
# OUTPUT_FILENAME = "movies.txt"


def download_webpage(url) -> str:
    #
    #   get webpage as text
    #
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                      "Version/14.0.2 Safari/605.1.15",
        "Accept-Language": "en-US"
    }
    response = requests.get(url, headers=headers)
    _webpage = response.text
    return _webpage


def save_webpage(filename, _webpage) -> None:
    #
    #   save webpage to file
    #
    with open(filename, "w", encoding="utf-8") as fp:
        fp.write(_webpage)


def load_webpage(filename) -> str:
    #
    #   load webpage from file
    #
    with open(filename, encoding="utf-8") as fp:
        _webpage = fp.read()
        return _webpage


def get_webpage(url, cache=False, filename="webpage.txt"):
    if cache:
        try:
            #
            #   if file exist, already downloaded, goto else:
            #
            with open(filename) as fp:
                pass
        except FileNotFoundError:
            print(f"{filename} does not exists")
            print(f"downloading {url}...")
            _webpage = download_webpage(URL)
            print(f"saving {url} to {filename}...")
            save_webpage(filename, _webpage)
        else:
            print(f"{filename} exists")
            print(f"loading {url} from {filename}...")
            _webpage = load_webpage(filename)
        finally:
            pass
            return _webpage
    else:
        print(f"downloading {url}...")
        _webpage = download_webpage(URL)
        return _webpage


# webpage = get_webpage(URL)
webpage = get_webpage(URL, cache=True,  filename="zillow.html")
print(webpage)
soup = BeautifulSoup(webpage, "html.parser")



