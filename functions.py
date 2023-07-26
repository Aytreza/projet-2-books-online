import requests
from bs4 import BeautifulSoup
from constants import ALL_CATEGORIES


def print_user_choices():
    categories_list = []
    for i in range(1, len(ALL_CATEGORIES)+1):
        categories_list.append(ALL_CATEGORIES[i])
    max_length = len(sorted(categories_list, key=lambda x: len(x), reverse=True)[0])
    text = ""
    for i in range(0, len(categories_list)):
        if i % 5 == 0:
            text += "\n"
        category = categories_list[i]
        number_of_spaces = max_length - len(category) + 3
        text += f"{i + 1} : {category}"
        for j in range(0, number_of_spaces):
            text += " "
        if i < 9:
            text += " "
    print(text)


def pounds_to_euros(pounds):
    return round(pounds * 0.86, 2)


def next_page_url_suffix(soup_object):
    # Détermine si il y a une prochaine page dans la catégorie active
    link = soup_object.find("li", class_="next")
    if not link:
        return None
    # Exemple : page-2.html
    return link.find("a")["href"]


def save_to_csv(list_of_books_infos):
    csv = "product_page_url; universal_product_code; title; price_including_tax; price_excluding_tax; number_available; category; review_rating; image_url; product_description;\n"
    for books_infos in list_of_books_infos:
        for i in range(0, len(books_infos)):
            book_info = books_infos[i]
            # Suppression des ; dans les titres et descriptions pour éviter des conflits avec les séparateurs du fichier csv
            if i == 2 or i == 9:
                csv += f"{book_info.replace(';', ',')}; "
            else:
                csv += f"{book_info}; "
        csv += "\n"
    file = open("output.csv", "w")
    file.write(csv)
    file.close()


def get_page_infos(url, category):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    product_page = soup.find("article", class_="product_page")

    title = product_page.find("h1").text
    image_url = product_page.find(id="product_gallery").find("img")["src"]
    product_description = product_page.find(id="product_description").find_next_sibling("p").text
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
        category,
        review_rating,
        image_url,
        product_description,
    )