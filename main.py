from classes import Category
from functions import print_user_choices, ask_user_choice, get_categories, get_page_infos
import os
import shutil


def scrap_category(index):
    name, url = categories[index]
    category = Category(name, url)
    pages_infos = []
    print()
    print("Chargement...")
    for book_url in category.books_url():
        print(book_url)
        pages_infos.append(get_page_infos(book_url, category))
    category.save_to_csv(pages_infos)
    print()
    print(f"Fichier {category.name}.csv créé.")


categories = get_categories()

# Suppression du dossier "output"
if os.path.exists('output') and os.path.isdir('output'):
    shutil.rmtree('output')

# Création des répertoires
os.mkdir('output')
os.chdir('output')
os.mkdir('csv')
os.mkdir('images')
os.chdir('images')
for i in range(0, len(categories)):
    os.mkdir(categories[i][0])
    # dossier courant = "output"
os.chdir(os.path.dirname(os.getcwd()))


# Choix des catégories à extraire
print_user_choices(categories)
user_choice = ask_user_choice()





if user_choice != 0:
    # Seule la catégorie choisie est extraite
    scrap_category(user_choice - 1)
    # Toutes les catégories sont extraites
else:
    for i in range(0, len(categories)):
        scrap_category(i)
