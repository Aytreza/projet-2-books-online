from functions.scraping import get_categories, scrap_category
from functions.user_interface import ask_user_choice, print_user_choices
import os
import shutil
from tqdm import tqdm

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
    category_name, category_url = categories[user_choice - 1]
    scrap_category(category_name, category_url)
    # Toutes les catégories sont extraites
else:
    for category_name, category_url in categories:
        scrap_category(category_name, category_url)
