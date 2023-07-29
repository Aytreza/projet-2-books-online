from functions.scraping import get_categories, scrap_category
from functions.user_interface import ask_user_choice, print_user_choices
import os
import shutil

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
    scrap_category(categories, user_choice - 1)
    # Toutes les catégories sont extraites
else:
    for i in range(0, len(categories)):
        scrap_category(categories, i)
