import requests
from bs4 import BeautifulSoup

from constants import ALL_CATEGORIES
from functions import next_page_url


class Category:
    BASE_URL_CATEGORIES = "http://books.toscrape.com/catalogue/category/books/"
    BASE_URL_BOOKS = "http://books.toscrape.com/catalogue/"

    def __init__(self, index: int):
        self.index = index
        self.name = ALL_CATEGORIES[index]

    def url(self):
        name = self.name
        url_suffix = f"{name.lower().replace(' ', '-')}_{self.index}/index.html"
        return f"{Category.BASE_URL_CATEGORIES}{url_suffix}"

    def parse_book_url(relative_path: str):
        return f"{Category.BASE_URL_BOOKS}{relative_path.replace('../', '')}"

    def books_url(self, url="", urls=[]):
        if url == "":
            url = self.url()
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        products = soup.find_all("article", class_="product_pod")
        for product in products:
            urls.append(product.find("h3").find("a")['href'])
        next_page_name = next_page_url(soup)
        if next_page_name:
            next_url = url.replace("index.html", next_page_name)
            return self.books_url(next_url, urls)
        # return urls
        urls_absolute = []
        for url_relative in urls:
            urls_absolute.append(Category.parse_book_url(url_relative))
        return urls_absolute
