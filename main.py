from classes import Category
from functions import get_page_infos, save_to_csv

category = Category(3)
pages_infos = []
for book_url in category.books_url():
    pages_infos.append(get_page_infos(book_url, category.name))
save_to_csv(pages_infos)

# pages_infos = []
# for url in urls:
#     parsed_url = parse_relative_path("http://books.toscrape.com/catalogue/", url)
# print(get_page_infos(parsed_url))
# pages_infos.append(get_page_infos(parsed_url))
#
# print(pages_infos)
#
# save_to_json(pages_infos)
