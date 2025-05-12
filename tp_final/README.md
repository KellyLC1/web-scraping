# Librairie en ligne - Application Web

Cette application permet de gérer une librairie en ligne avec une interface interactive. Elle se connecte à une base de données MongoDB pour afficher, filtrer et analyser des livres. L'application utilise **Streamlit** pour l'interface utilisateur, **Matplotlib** et **Seaborn** pour la visualisation des données, et **Pandas** pour la gestion des données.

## Fonctionnalités

### 1. **Page Librairie** :
- **Barre de recherche** : Permet de rechercher un livre par titre.
- **Filtres** : Vous pouvez filtrer les livres par note minimale, prix maximum et genre.
- **Affichage des livres** : Les livres sont affichés sous forme de cartes avec des informations détaillées telles que le titre, le prix, la note, et la disponibilité.
- **Téléchargement des données** : Un bouton dans la barre latérale permet de télécharger les données sous forme de fichier CSV.

### 2. **Page Statistiques** :
- **Répartition des livres par note** : Un graphique montrant la répartition des livres selon leur note.
- **Nombre de livres par genre** : Un graphique en barre indiquant combien de livres existent dans chaque genre.
- **Prix moyen par genre** : Un graphique montrant le prix moyen des livres par genre.
- **Top 5 des livres les plus chers** : Un tableau listant les livres les plus chers.
- **Statistiques supplémentaires** :
  - Nombre total de livres.
  - Nombre de livres disponibles et indisponibles.
  - Distribution des prix des livres.
  - Top 5 des livres les mieux notés.

## Prérequis

1. **Python 3.x**
2. **MongoDB** (base de données des livres)
3. **Streamlit** : Pour l'interface utilisateur.
4. **Pandas** : Pour la gestion des données.
5. **Matplotlib et Seaborn** : Pour les visualisations.

## Installation

Clonez ce repository et installez les dépendances requises :

git clone https://github.com/KellyLC1/web-scraping/tree/main/tp_final
cd tp_final
pip install -r requirements.txt

Exécution
Lancez l'application Streamlit avec la commande suivante :

streamlit run app.py

Structure du projet

tp_final/
│
├── app.py               
├── analytics.txt     
├── data.csv               
└── scraper.py                
└── README.md            
           

