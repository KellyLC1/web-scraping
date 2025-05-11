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

git clone https://github.com/votre-repository/librairie-en-ligne.git
cd librairie-en-ligne
pip install -r requirements.txt
Assurez-vous d'avoir MongoDB installé et exécuté localement avec la base de données librairie et la collection livres configurée.

Exécution
Lancez l'application Streamlit avec la commande suivante :

bash
Copier
Modifier
streamlit run app.py
Cela ouvrira l'application dans votre navigateur.

Structure du projet
bash
Copier
Modifier
librairie-en-ligne/
│
├── app.py               # Application principale Streamlit
├── requirements.txt     # Liste des dépendances Python
├── data/                # Dossier contenant les données MongoDB
└── README.md            # Documentation du projet
Contribuer
Forkez le projet.

Créez une branche pour votre fonctionnalité (git checkout -b feature/ma-nouvelle-fonctionnalite).

Committez vos changements (git commit -am 'Ajout d\'une fonctionnalité').

Poussez sur la branche (git push origin feature/ma-nouvelle-fonctionnalite).

Ouvrez une Pull Request.

License
Distribué sous la licence MIT. Voir LICENSE pour plus de détails.

yaml
Copier
Modifier

---

### **Google Doc** :

J'ai créé un **Google Doc** pour documenter davantage le projet. Tu peux y accéder via ce lien : [Google Doc - Documentation Librairie en ligne](https://docs.google.com/document/d/1x4FVPl0ok8Bb77I3t-JrcFmpv9EIs6lOC2wJ0-37BbI/edit?usp=sharing).

Tu y trouveras des détails supplémentaires sur le fonctionnement de l'application, ainsi que des instructions pour la configuration de MongoDB et l'ajout de données.

---

N'hésite pas à me dire si tu souhaites ajouter des informations spécifiques à ces documents !