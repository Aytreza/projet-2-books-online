import requests
from bs4 import BeautifulSoup

from constants import BASE_URL
from functions.utils import replace_suffix, relative_to_absolute_path
from functions.write import save_to_jpg, save_to_csv
from tqdm import tqdm


def next_page_url(soup_object):
    # Détermine si il y a une prochaine page dans la catégorie active
    link = soup_object.find("li", class_="next")
    if not link:
        return None
    # Exemple : page-2.html
    return link.find("a")["href"]


def get_books_infos(url, category):
    try:
        page = requests.get(url, timeout=5)
    except TimeoutError:
        print("Le serveur a mis trop de temps à répondre: " + url)
        return None
    except:
        print("Une erreur est survenue: " + url)
        return None
    soup = BeautifulSoup(page.content, "html.parser")
    product_page = soup.find("article", class_="product_page")

    #############  EXTRACT  #############

    _title = product_page.find("h1").text
    _image_url = product_page.find(id="product_gallery").find("img")["src"]
    _product_description = product_page.find(id="product_description")
    _review_rating = product_page.find(class_="star-rating")["class"][1]
    infos = {}
    for row in product_page.find("table", class_="table").find_all("tr"):
        name, value = (row.find("th").text, row.find("td").text)
        infos[name] = value
    _universal_product_code = infos["UPC"]
    _price_including_tax = infos["Price (incl. tax)"]
    _price_excluding_tax = infos["Price (excl. tax)"]
    _number_available = infos["Availability"]

    ############# TRANSFORM #############

    title = _title
    product_description = "" if _product_description is None else _product_description.find_next_sibling("p").text
    universal_product_code = _universal_product_code
    price_including_tax = float(_price_including_tax[1:])
    price_excluding_tax = float(_price_excluding_tax[1:])
    number_available = int(_number_available[10:12])
    match _review_rating:
        case "One":   review_rating = 1
        case "Two":   review_rating = 2
        case "Three": review_rating = 3
        case "Four":  review_rating = 4
        case "Five":  review_rating = 5
        case _: review_rating = -1
    image_url = BASE_URL + _image_url.replace('../','')

    save_to_jpg(image_url, title, category)

    return (
        url,
        universal_product_code,
        title,
        price_including_tax,
        price_excluding_tax,
        number_available,
        category,
        review_rating,
        image_url,
        product_description,
    )


def get_categories():
    page = requests.get(BASE_URL)
    soup_object = BeautifulSoup(page.content, "html.parser")
    categories_elts = soup_object.find("div", class_="side_categories").find("ul", class_="nav nav-list").find(
        "ul").find_all("a")
    categories = []
    for i in range(0, len(categories_elts)):
        category = categories_elts[i]
        categories.append((
            category.text.lstrip().rstrip(),
            BASE_URL + category["href"]
        ))
    return categories


def get_books_url(category_url, books_urls=None):
    # Si url == None, premier passage dans la fonction
    if books_urls is None:
        books_urls = []
    page = requests.get(category_url)
    soup_object = BeautifulSoup(page.content, "html.parser")
    products = soup_object.find_all("article", class_="product_pod")
    for product in products:
        books_urls.append(product.find("h3").find("a")['href'])
    # Après avoir bouclé sur les livres de la page active, on vérifie si la  page suivante existe
    _next_page_url = next_page_url(soup_object)
    if _next_page_url:
        next_url = replace_suffix(category_url, _next_page_url)
        # Appel récursif si la page suivante existe
        return get_books_url(next_url, books_urls)
    urls_absolute = []
    for url_relative in books_urls:
        urls_absolute.append(relative_to_absolute_path(url_relative))
    return urls_absolute


def scrap_category(category_name, category_url):
    pages_infos = []
    for book_url in tqdm(get_books_url(category_url), position=0, desc=category_name):
        pages_infos.append(get_books_infos(book_url, category_name))
    save_to_csv(category_name, pages_infos)
