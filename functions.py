import requests
from bs4 import BeautifulSoup

from constants import BASE_URL, BASE_URL_BOOKS


def ask_user_choice():
    while True:
        choice_str = input("Choisissez la catégorie (de 0 à 50) : ")
        try:
            choice_int = int(choice_str)
        except ValueError:
            print("ERREUR : choisissez un nombre entre 1 et 50")
        else:
            if choice_int < 0 or choice_int > 50:
                print("ERREUR : choisissez un nombre entre 1 et 50")
            else:
                return choice_int


def print_user_choices(categories):
    sorted_categories = sorted(categories, key=lambda x: len(x[0]), reverse=True)
    max_length = len(sorted_categories[0][0])
    text = "0 : Toutes les catégories"
    for i in range(0, len(categories)):
        if i % 5 == 0:
            text += "\n"
        category = categories[i][0]
        number_of_spaces = max_length - len(category) + 3
        text += f"{i + 1} : {category}"
        for j in range(0, number_of_spaces):
            text += " "
        if i < 9:
            text += " "
    print(text)


def pounds_to_euros(pounds):
    return round(pounds * 0.86, 2)


def replace_suffix(url: str, new_suffix):
    return url[0:url.rfind("/") + 1] + new_suffix


def next_page_url(soup_object):
    # Détermine si il y a une prochaine page dans la catégorie active
    link = soup_object.find("li", class_="next")
    if not link:
        return None
    # Exemple : page-2.html
    return link.find("a")["href"]


def save_to_jpg(url, title, category):
    image_data = requests.get(url).content
    # Suppression des caractère interdits, limite du nom de fichier à 80 caractères
    title = title.replace(":", " -").replace("/", " -").replace("\\", "").replace('"', "").replace("*", "-").replace("?", ".")[:80]
    path = f"images/{category.name}/{title}.jpg"
    file = open(path, "wb")
    file.write(image_data)
    file.close()


def get_page_infos(url, category):
    try:
        page = requests.get(url, timeout=5)
    except TimeoutError:
        print("Le serveur a mis trop de temps à répondre")
        return None
    except:
        print("Une erreur est survenue")
        return None
    soup = BeautifulSoup(page.content, "html.parser")
    product_page = soup.find("article", class_="product_page")

    title = product_page.find("h1").text
    image_url = "http://books.toscrape.com/" + product_page.find(id="product_gallery").find("img")["src"].replace('../','')
    save_to_jpg(image_url, title, category)
    try:
        product_description = product_page.find(id="product_description").find_next_sibling("p").text
    except:
        product_description = ""
    match product_page.find(class_="star-rating")["class"][1]:
        case "One":   review_rating = 1
        case "Two":   review_rating = 2
        case "Three": review_rating = 3
        case "Four":  review_rating = 4
        case "Five":  review_rating = 5
        case _: review_rating = -1
    infos_table = product_page.find("table", class_="table")
    table_rows = infos_table.find_all("tr")
    infos = {}
    for row in table_rows:
        name, value = (row.find("th").text, row.find("td").text)
        infos[name] = value
    universal_product_code = infos["UPC"]
    price_including_tax = pounds_to_euros(float(infos["Price (incl. tax)"][1:]))
    price_excluding_tax = pounds_to_euros(float(infos["Price (excl. tax)"][1:]))
    number_available = int(infos["Availability"][10:12])

    return (
        url,
        universal_product_code,
        title,
        price_including_tax,
        price_excluding_tax,
        number_available,
        category.name,
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

def relative_to_absolute_path(relative_path: str):
    # Exemple :
    # ../../../tipping-the-velvet_999/index.html
    # http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html
    return f"{BASE_URL_BOOKS}{relative_path.replace('../', '')}"


