from classes import Category
from functions import get_page_infos, save_to_csv, print_user_choices, ask_user_choice, save_to_jpg
from constants import ALL_CATEGORIES
import os


# Création des dossiers si ils n'existent pas
try:
    os.mkdir('output')
    os.chdir('output')
    os.mkdir('csv')
    os.mkdir('images')
except FileExistsError:
    pass


# Choix des catégories à extraire
print_user_choices()
user_choice = ask_user_choice()
if user_choice != 0:
    category = Category(user_choice)
    pages_infos = []
    print()
    print("Chargement...")

    for book_url in category.books_url():
        print(book_url)
        pages_infos.append(get_page_infos(book_url, category.name))
    save_to_csv(pages_infos, category)
    print()
    print("Fichier créé.")

# Toutes les catégories sont extraites
else:
    for i in range(1, len(ALL_CATEGORIES) + 1):
        category = Category(i)
        pages_infos = []
        print()
        print(category.name)
        print("Chargement...")

        for book_url in category.books_url():
            print(book_url)
            page_infos = get_page_infos(book_url, category.name)
            # page_infos = None en cas de problème avec la requête dans get_page_infos
            if page_infos:
                pages_infos.append(page_infos)
        save_to_csv(pages_infos, category)
        print(f"Fichier {category.index}-{category.name}.csv créé.")
