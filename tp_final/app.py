import pandas as pd
import streamlit as st
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["librairie"]
collection = db["livres"]
data = list(collection.find())

# Création d'un DataFrame
df_mongo = pd.DataFrame(data)

# Nettoyer les genres
genres = df_mongo["Genre"].dropna().unique().tolist()
genres.sort()

# Sidebar pour la navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Choisir une section", ("Librairie", "Stats"))

# Bouton de téléchargement dans la sidebar
if not df_mongo.empty:
    csv = df_mongo.drop(columns=['_id']).to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="💾 Télécharger les données en CSV",
        data=csv,
        file_name='livres.csv',
        mime='text/csv'
    )

# Affichage de la page en fonction de la section choisie
if section == "Librairie":
    st.header("📚 Librairie en ligne")

    # Barre de recherche
    search = st.text_input("", placeholder="🔎 Rechercher un livre par titre")

    # Filtres
    col1, col2, col3 = st.columns(3)
    with col1:
        note_min = st.slider("🎯 Note minimale", 0, 5, 0)
    with col2:
        prix_max = st.slider("💰 Prix maximum (£)", 0, 100, 100)
    with col3:
        selected_genre = st.selectbox("📚 Genre", ["Tous"] + genres)

    # Filtrage
    filtered_df = df_mongo[
        df_mongo["Titre"].str.contains(search, case=False, na=False) &
        (df_mongo["Note"] >= note_min) &
        (df_mongo["Prix (£)"] <= prix_max)
    ]

    if selected_genre != "Tous":
        filtered_df = filtered_df[filtered_df["Genre"] == selected_genre]

    st.markdown(f"### {len(filtered_df)} livres trouvés")

    # Style global
    st.markdown("""
        <style>
        .book-card {
            height: 500px;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            background-color: #f0f0f0;
            color: #000000;
            transition: transform 0.3s ease-in-out;
        }
        .book-card:hover {
            transform: scale(1.02);
        }
        .book-card img {
            width: 100%;
            height: 200px;
            border-radius: 10px;
            object-fit: cover;
        }
        .book-card h4 {
            margin-bottom: 5px;
            color: #222;
            font-size: 1.1em;
        }
        </style>
    """, unsafe_allow_html=True)

    # Affichage en cartes (3 colonnes par ligne)
    cols = st.columns(3)

    for i, (_, row) in enumerate(filtered_df.iterrows()):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="book-card">
                <img src="{row['Image_URL']}" alt="{row['Titre']}">
                <h4>📖 {row['Titre']}</h4>
                <p>💸 <strong>{row['Prix (£)']} £</strong></p>
                <p>⭐️ {int(row['Note'])} / 5</p>
                <p>🏷️ {row['Genre']}</p>
                <p>{'✅ Disponible' if 'In stock' in row['Disponibilité'] else '❌ Indisponible'}</p>
            </div>
            """, unsafe_allow_html=True)

elif section == "Stats":
    st.header("📈 Analyse des livres")

    if not df_mongo.empty:
        # 1. Répartition des livres par note
        fig1, ax1 = plt.subplots()
        sns.countplot(data=df_mongo, x="Note", palette="Blues", ax=ax1)
        ax1.set_title("Répartition des livres par note")
        st.pyplot(fig1)

        # 2. Nombre de livres par genre
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        genre_counts = df_mongo["Genre"].value_counts()
        sns.barplot(x=genre_counts.index, y=genre_counts.values, palette="coolwarm", ax=ax2)
        ax2.set_title("Nombre de livres par genre")
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
        st.pyplot(fig2)

        # 3. Prix moyen par genre
        fig3, ax3 = plt.subplots(figsize=(10, 4))
        avg_price = df_mongo.groupby("Genre")["Prix (£)"].mean().sort_values(ascending=False)
        sns.barplot(x=avg_price.index, y=avg_price.values, palette="mako", ax=ax3)
        ax3.set_title("Prix moyen par genre")
        ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha='right')
        st.pyplot(fig3)

        # 4. Genre le plus courant
        top_genre = df_mongo["Genre"].value_counts().idxmax()
        st.markdown(f"**➡️ Genre le plus fréquent :** {top_genre}")

        # 5. Moyenne des prix
        mean_price = df_mongo["Prix (£)"].mean()
        st.markdown(f"**➡️ Prix moyen :** £{mean_price:.2f}")

        # 6. Top 5 des livres les plus chers
        st.markdown("**➡️ Top 5 des livres les plus chers :**")
        top_5_expensive_books = df_mongo[["Titre", "Prix (£)"]].sort_values(by="Prix (£)", ascending=False).head(5)
        st.write(top_5_expensive_books)

        # --- Statistiques supplémentaires ---

        # 7. Nombre total de livres
        total_books = len(df_mongo)
        st.markdown(f"**➡️ Nombre total de livres :** {total_books}")

        # 8. Nombre de livres par disponibilité
        available_books = df_mongo[df_mongo["Disponibilité"].str.contains("In stock", na=False)]
        unavailable_books = df_mongo[~df_mongo["Disponibilité"].str.contains("In stock", na=False)]

        st.markdown(f"**➡️ Livres disponibles :** {len(available_books)}")
        st.markdown(f"**➡️ Livres indisponibles :** {len(unavailable_books)}")

        # 9. Distribution des prix
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.histplot(df_mongo["Prix (£)"], kde=True, color="purple", ax=ax4)
        ax4.set_title("Distribution des prix des livres")
        st.pyplot(fig4)

        # 10. Top 5 des livres les plus populaires (basé sur la note)
        top_5_books_by_rating = df_mongo[["Titre", "Note"]].sort_values(by="Note", ascending=False).head(5)
        st.markdown("**➡️ Top 5 des livres les mieux notés :**")
        st.write(top_5_books_by_rating)

    else:
        st.warning("Aucune donnée trouvée dans MongoDB.")
