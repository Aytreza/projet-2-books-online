import requests
from bs4 import BeautifulSoup

from functions import next_page_url_suffix, replace_suffix


class Category:
    BASE_URL = "http://books.toscrape.com/catalogue/"
    BASE_URL_CATEGORIES = f"{BASE_URL}category/books/"

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

    def relative_to_absolute_path(relative_path: str):
        # Exemple :
        # ../../../tipping-the-velvet_999/index.html
        # http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html
        return f"{Category.BASE_URL}{relative_path.replace('../', '')}"

    def books_url(self, url="", urls_relative=None):

        """
        QUESTION : si urls_relative initialisé à [], pourquoi urls_relative recommence au début pour chaque catégorie?
        -> chaque fichier commence par le contenu de celui d'avant
        """

        """
        Si url == None, premier passage dans la fonction, l'url devient self.url
        Sinon, cela implique un appel récursif avec l'url de la page suivante
        """
        if urls_relative is None:
            urls_relative = []
        if url == "":
            url = self.url
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
