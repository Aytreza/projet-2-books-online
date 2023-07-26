import requests
from bs4 import BeautifulSoup

from constants import ALL_CATEGORIES
from functions import next_page_url_suffix, replace_suffix


class Category:
    BASE_URL = "http://books.toscrape.com/catalogue/"
    BASE_URL_CATEGORIES = f"{BASE_URL}category/books/"

    def __init__(self, index: int):
        self.index = index
        self.name = ALL_CATEGORIES[index]

    def url(self):
        name = self.name
        # Exemple :
        # Historical Fiction
        # historical-fiction_4/index.html
        url_suffix = f"{name.lower().replace(' ', '-')}_{self.index+1}/index.html" # index + 1 car urls commencent à 2
        return f"{Category.BASE_URL_CATEGORIES}{url_suffix}"

    def relative_to_absolute_path(relative_path: str):
        # Exemple :
        # ../../../tipping-the-velvet_999/index.html
        # http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html
        return f"{Category.BASE_URL}{relative_path.replace('../', '')}"

    def books_url(self, url="", urls_relative=[]):
        """
        Si url == "", premier passage dans la fonction, l'url devient self.url
        Sinon, cela implique un appel récursif avec l'url de la page suivante
        """
        if url == "":
            url = self.url()
        page = requests.get(url)
        soup_object = BeautifulSoup(page.content, "html.parser")
        products = soup_object.find_all("article", class_="product_pod")
        for product in products:
            urls_relative.append(product.find("h3").find("a")['href'])
        # Après avoir bouclé sur les livres de la page active, on vérifie si la  page suivante existe
        _next_page_url_suffix = next_page_url_suffix(soup_object)
        if _next_page_url_suffix:
            next_url = replace_suffix(url, _next_page_url_suffix)
            # Appel récursif si la page suivante existe
            return self.books_url(next_url, urls_relative)
        urls_absolute = []
        for url_relative in urls_relative:
            urls_absolute.append(Category.relative_to_absolute_path(url_relative))
        return urls_absolute
