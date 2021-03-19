class Cache:
    def __init__(self, filename, enabled):
        print(f"{__class__.__name__}: filename={filename}, enabled={enabled}")
        self.filename = filename
        self._enabled = enabled
        self.webpage = ""

    def is_enabled(self):
        print(f"{__class__.__name__}: {'is' if self._enabled else 'is NOT'} enabled ")
        return self._enabled

    def enable(self):
        print(f"{__class__.__name__}: enabling cache")
        self._enabled = True

    def disable(self):
        print(f"{__class__.__name__}: disabling cache")
        self._enabled = False

    def is_cached(self):
        try:
            with open(self.filename):
                print(f"{__class__.__name__}: {self.filename} is cached")
                return True
        except FileNotFoundError:
            print(f"{__class__.__name__}: {self.filename} is NOT cached")
            return False

    def save(self) -> None:
        #
        #   save webpage to file
        #
        print(f"{__class__.__name__}: saving {self.filename}")
        with open(self.filename, "w", encoding="utf-8") as fp:
            fp.write(self.webpage)

    def update(self, webpage):
        print(f"{__class__.__name__}: updating {self.filename}")
        self.webpage = webpage
        self.save()

    def load(self) -> str:
        #
        #   load webpage from file
        #
        print(f"{__class__.__name__}: loading from {self.filename}")
        with open(self.filename, encoding="utf-8") as fp:
            self.webpage = fp.read()
            return self.webpage

    def get(self, update=False, webpage=""):
        print(f"{__class__.__name__}: getting page update={update}")
        if update:
            self.update(webpage)
        self.webpage = self.load()
        return self.webpage
