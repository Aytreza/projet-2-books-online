import requests
from bs4 import BeautifulSoup
from functions import next_page_url, replace_suffix, relative_to_absolute_path


class Category:

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

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
        _next_page_url_suffix = next_page_url(soup_object)
        if _next_page_url_suffix:
            next_url = replace_suffix(url, _next_page_url_suffix)
            # Appel récursif si la page suivante existe
            return self.books_url(next_url, urls_relative)
        urls_absolute = []
        for url_relative in urls_relative:
            urls_absolute.append(relative_to_absolute_path(url_relative))
        return urls_absolute

    def save_to_csv(self, books_infoss):
        csv = "product_page_url; universal_product_code; title; price_including_tax; price_excluding_tax; number_available; category; review_rating; image_url; product_description;\n"
        for books_infos in books_infoss:
            for i in range(0, len(books_infos)):
                book_info = books_infos[i]
                # Suppression des ; dans les titres et descriptions pour éviter des conflits avec les séparateurs du fichier csv
                if i == 2 or i == 9:
                    csv += f"{book_info.replace(';', ',')}; "
                else:
                    csv += f"{book_info}; "
            csv += "\n"
        file = open(f"csv/{self.name}.csv", "w", encoding='utf-8')
        file.write(csv)
        file.close()