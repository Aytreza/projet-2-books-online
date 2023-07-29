from constants import BASE_URL_BOOKS


def relative_to_absolute_path(relative_path: str):
    # Exemple :
    # ../../../tipping-the-velvet_999/index.html
    # http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html
    return f"{BASE_URL_BOOKS}{relative_path.replace('../', '')}"


def replace_suffix(url: str, new_suffix):
    return url[0:url.rfind("/") + 1] + new_suffix


def pounds_to_euros(pounds):
    return round(pounds * 0.86, 2)
