from functions import print_user_choices, ask_user_choice, get_categories, get_page_infos, get_books_url, save_to_csv
import os
import shutil

categories = get_categories()


def scrap_category(index):
    category_name, category_url = categories[index]
    pages_infos = []
    print()
    print("Chargement...")
    for book_url in get_books_url(category_url):
        print(book_url)
        pages_infos.append(get_page_infos(book_url, category_name))
    save_to_csv(category_name, pages_infos)
    print()
    print(f"Fichier {category_name}.csv créé.")


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
