# Books Online Scaper

Books Online Scaper est un outil permettant d'automatiser le téléchargement d'informations sur un site concurrent (http://books.toscrape.com/), 
afin de pouvoir notamment comparer les tarifs de Books Online avec les-leurs.

## Installation
```bash
Installer la dernière version de Python (https://www.python.org/)

Ouvrir un terminal à la racine du dossier qui contiendra le projet.

git clone https://github.com/Aytreza/projet-2-books-online.git

# Installation et activation de l'environnement virtuel venv
# Windows : 
python -m venv venv
.\venv\scripts\activate
# MacOS: 
python3 -m venv venv
source venv/bin/activate

# Installation des librairies externes
pip install requests
pip install bs4

# Exécution du script :
python main.py
```
## Utilisation

Au lancement du scipt, la console affiche une liste de choix à l'utilisateur:

Choisir 0 pour télécharger l'intégralité des livres du site.

Choisir un nombre entre 1 et 50, correspondant à une catégorie particulière à télécharger.

Un dossier "output" contenant les dossiers "csv" et "images" est créé à la racine du projet.

Les données extraites apparaissent sous forme de fichiers csv, nommés par catégorie.

Les images des livres apparaissent dans des sous dossiers du dossier "images", correspondant chacun à une catégorie.

Attention : à chaque lancement du script, le dossier "output" et son contenu sont supprimés.


