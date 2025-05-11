import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient


base_url = "https://books.toscrape.com/catalogue/page-{}.html"
all_books = []

for page in range(1, 51):  # réduire le nombre de page pour les tests car sinon ça prend trop de temps
    print(f"📄 Scraping page {page}")
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.select("article.product_pod")

    for book in books:
        title = book.h3.a["title"]

        # URL de l'image
        image_url = book.select_one("img")["src"]
        if not image_url.startswith("http"):
            full_image_url = "https://books.toscrape.com/" + image_url.replace("../", "")
        else:
            full_image_url = image_url

        # Prix
        price_raw = book.select_one(".price_color").text.strip()
        price = price_raw.encode('ascii', 'ignore').decode().replace("£", "")

        # Disponibilité
        availability = book.select_one(".availability").text.strip()

        # Note
        rating_class = book.select_one("p.star-rating")["class"][1]
        ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

        # Lien vers la fiche produit
        detail_url = "https://books.toscrape.com/catalogue/" + book.h3.a["href"]

        # Récupérer le genre depuis la page du produit
        detail_resp = requests.get(detail_url)
        detail_soup = BeautifulSoup(detail_resp.text, "html.parser")
        breadcrumb = detail_soup.select("ul.breadcrumb li a")
        genre = breadcrumb[2].text.strip() if len(breadcrumb) > 2 else "Inconnu"

        all_books.append({
            "Titre": title,
            "Prix (£)": float(price),
            "Disponibilité": availability,
            "Note": ratings.get(rating_class, 0),
            "Image_URL": full_image_url,
            "Genre": genre
        })

df = pd.DataFrame(all_books)
df.to_csv("data.csv", index=False)
print("✅ Fichier data.csv créé avec succès.")

# Connexion à MongoDB local (ou remplace par MongoDB Atlas si besoin)
client = MongoClient("mongodb://localhost:27017/")
db = client["librairie"]
collection = db["livres"]

# Vider l'ancienne collection
collection.delete_many({})

# Insertion des livres
collection.insert_many(df.to_dict("records"))
print("✅ Données insérées dans MongoDB")
