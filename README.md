# Books Online Scaper

Books Online Scaper est un outil permettant d'automatiser le téléchargement d'informations sur un site concurrent (http://books.toscrape.com/) à des fins d'analyse marketing.

## Installation
```bash
Installer Python v3.10 ou supérieure
Installer Git

Ouvrir un terminal à la racine du répertoire qui contiendra le projet.

git clone https://github.com/Aytreza/projet-2-books-online.git

# Installation et activation de l'environnement virtuel venv
# Windows : 
python -m venv venv
.\venv\scripts\activate
# MacOS et Linux: 
python3 -m venv venv
source venv/bin/activate

# Installation des librairies externes
voir fichier "requirements.txt"

# Exécution du script :
python main.py
```
## Utilisation

Au lancement du scipt, la console affiche une liste de choix à l'utilisateur:

Pour télécharger l'intégralité des données du site, choisir "0", sinon choisir une catégorie par le numéro correspondant (entre 1 et 50).

Un répertoire "output" contenant les sous-répertoires "csv" et "images" est créé à la racine du projet.

Les données extraites apparaissent sous forme de fichiers csv, nommés par catégorie.

Les fichiers csv utilisent le séparateur ";" (point-virgule). 

Les images des livres apparaissent dans des sous-répertoires du dossier "images", correspondant chacun à une catégorie.

Attention : à chaque lancement du script, le dossier "output" et son contenu sont supprimés.


