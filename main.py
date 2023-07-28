from classes import Category
from functions import get_page_infos, save_to_csv, print_user_choices, ask_user_choice, save_to_jpg, get_categories
import os
import shutil


categories = get_categories()


# Suppression du dossier "output"
if os.path.exists('output') and os.path.isdir('output'):
    shutil.rmtree('output')
try:
    # Création des répertoires
    os.mkdir('output')
    os.chdir('output')
    os.mkdir('csv')
    os.mkdir('images')
    os.chdir('images')
    for i in range(0, len(categories)):
        os.mkdir(categories[i][0])
        # dossier courant = "ouput"
    os.chdir(os.path.dirname(os.getcwd()))
except FileExistsError:
    pass

# Choix des catégories à extraire
print_user_choices(categories)
user_choice = ask_user_choice()
if user_choice != 0:
    name, url = categories[user_choice - 1]
    category = Category(name, url)
    pages_infos = []
    print()
    print("Chargement...")
    for book_url in category.books_url():
        print(book_url)
        pages_infos.append(get_page_infos(book_url, category))
    save_to_csv(pages_infos, category)
    print()
    print("Fichier créé.")

# Toutes les catégories sont extraites
else:
    for i in range(0, len(categories)):
        name, url = categories[i]
        category = Category(name, url)
        pages_infos = []
        print()
        print(category.name)
        print("Chargement...")

        for book_url in category.books_url():
            print(book_url)
            page_infos = get_page_infos(book_url, category)
            # page_infos = None en cas de problème avec la requête dans get_page_infos
            if page_infos:
                pages_infos.append(page_infos)
        save_to_csv(pages_infos, category)
        print(f"Fichier {category.name}.csv créé.")
