from classes import Category
from functions import get_page_infos, save_to_csv, print_user_choices, ask_user_choice, replace_suffix
import os

# Création du dossier csv si il n'existe pas
try:
    os.mkdir('csv')
except FileExistsError:
    pass
print_user_choices()

user_choice = ask_user_choice()

category = Category(user_choice)
pages_infos = []
print()
print("Chargement...")

for book_url in category.books_url():
    print(book_url)
    pages_infos.append(get_page_infos(book_url, category.name))
save_to_csv(pages_infos, category)
print()
print("Fichier créé !")
