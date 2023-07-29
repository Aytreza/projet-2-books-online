import requests


def save_to_csv(name, books_infoss):
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
    file = open(f"csv/{name}.csv", "w", encoding='utf-8')
    file.write(csv)
    file.close()


def save_to_jpg(url, title, category):
    image_data = requests.get(url).content
    # Suppression des caractère interdits, limite du nom de fichier à 80 caractères
    title = title.replace(":", " -").replace("/", " -").replace("\\", "").replace('"', "").replace("*", "-").replace("?", ".")[:80]
    path = f"images/{category}/{title}.jpg"
    file = open(path, "wb")
    file.write(image_data)
    file.close()
