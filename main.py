from classes import Category
from functions import get_page_infos, save_to_csv, print_user_choices, ask_user_choice

print_user_choices()

user_choice = ask_user_choice()

category = Category(user_choice)
pages_infos = []
print()
print("Chargement...")
for book_url in category.books_url():
    pages_infos.append(get_page_infos(book_url, category.name))
save_to_csv(pages_infos)
print()
print("Fichier créé !")
