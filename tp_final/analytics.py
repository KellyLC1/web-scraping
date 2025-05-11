from pymongo import MongoClient
import pandas as pd

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["librairie"]
collection = db["livres"]

# Chargement des données
books = list(collection.find())
df = pd.DataFrame(books)

# Statistiques
print("📊 ANALYSE DES DONNÉES")

# Genre le plus courant
top_genre = df["Genre"].value_counts().idxmax()
print(f"➡️ Genre le plus fréquent : {top_genre}")

# Moyenne des prix
mean_price = df["Prix (£)"].mean()
print(f"➡️ Prix moyen : £{mean_price:.2f}")

# Répartition des notes
print("\n➡️ Répartition des livres par note :")
print(df["Note"].value_counts())

# Top 5 des livres les plus chers
print("\n➡️ Top 5 des livres les plus chers :")
print(df[["Titre", "Prix (£)"]].sort_values(by="Prix (£)", ascending=False).head(5))
