import streamlit as st
import pandas as pd
from app.utils.api import get_all_movies, get_user_recommendations, afficher_film_complet
from app.utils.charts import (
    plot_rating_distribution,
    plot_movies_per_year,
    plot_top_movies
)
from app.utils.logs import visual_log, display_logs
from datetime import datetime

st.set_page_config(
    page_title="HomeFlix",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("🎬 HomeFlix")
section = st.sidebar.radio("Navigation", [
    "🏠 Accueil",
    "📊 Statistiques des films",
    "🎯 Recommandations personnalisées",
    "📅 Statistiques par genre et année",
    "🎬 Détails d'un Film"
])

st.title("🎥 Tableau de bord de recommandations de films")
if section == "🏠 Accueil":
    st.markdown("""
    ### 🎥 Bienvenue sur HomeFlix !

    HomeFlix est une **plateforme de recommandation de films** qui vise à offrir à chaque utilisateur ou utilisatrice une expérience de visionnage **personnalisée**, en fonction de ses goûts et préférences.

    ---
    
    ## 🧭 Navigation
    - **📊 Statistiques des films** : Visualisez les tendances générales des films (notes, années de sortie, etc.).
    - **📅 Statistiques par genre et année** : Découvrez les meilleurs films pour un genre et une année donnée.
    - **🎯 Recommandations personnalisées** : Obtenez des suggestions personnalisées selon un ID utilisateur.
    - **🎬 Détails d'un Film : Permet d'afficher les détails d'un film par son ID

    ---
    
    ## 📁 Sources de données
    Les données utilisées dans ce projet proviennent de [TMDB](https://www.themoviedb.org/), enrichies pour permettre la recommandation de films.

    ---
    
    👨‍💻 Projet réalisé dans le cadre d’un projet pédagogique / personnel.

    """, unsafe_allow_html=True)
elif section == "📊 Statistiques des films":
    # Choix de la page pour charger les films
    page_num = st.sidebar.number_input(
        "Page des films à charger", min_value=1, max_value=100, value=1
    )
    st.subheader(f"Chargement des films - Page {page_num}")
    movies = get_all_movies(page=page_num)

    if not movies:
        st.error("Impossible de récupérer les films pour cette page.")
        visual_log("Échec du chargement des films", "ERROR")
    else:
        visual_log(f"{len(movies)} films chargés depuis la page {page_num}", "SUCCESS")
        st.subheader("Distribution des notes")
        plot_rating_distribution(movies)

        st.subheader("Nombre de films par année")
        plot_movies_per_year(movies)

        st.subheader("Top 10 des films les mieux notés")
        plot_top_movies(movies, top_n=10)

elif section == "🎯 Recommandations personnalisées":
    st.subheader("🔍 Rechercher des recommandations")

    with st.form("user_form"):
        user_id = st.number_input("Entrer l'ID utilisateur", min_value=1, step=1)
        num_reco = st.slider("Nombre de recommandations", 1, 20, 5)
        submitted = st.form_submit_button("Obtenir les recommandations")

    if submitted:
        try:
            reco_user = get_user_recommendations(user_id, num_reco)
            recommendations = reco_user["recommendations"]
            
            if recommendations:
                st.success(f"Voici {len(recommendations)} recommandations pour l'utilisateur {user_id}:")
                
                # Créer des colonnes pour l'affichage des films
                cols = st.columns(5)  # 5 films par ligne
                for i, film in enumerate(recommendations):
                    with cols[i % 5]:
                        st.write(film['title'])
                        st.write(film['movie_id'])
                        # Affiche l'affiche si disponible
                        poster = film.get('poster_path')
                        if poster:
                            image_url = f"https://image.tmdb.org/t/p/w300{poster}"
                            st.image(image_url, width=120)

                # Ajouter un petit écart entre les lignes de recommandations
                st.write("")  # Ligne vide pour un espacement
            else:
                st.warning("Aucune recommandation trouvée pour cet utilisateur.")
        except Exception as e:
            st.error(f"Erreur lors de la récupération des recommandations : {e}")


elif section == "📅 Statistiques par genre et année":
    st.subheader("🎞️ Filtrer par genre et année")

    genre = st.text_input("Genre (en anglais)", value="Action")
    year = st.number_input("Année", min_value=1930, max_value=2026, value=2020)

    if st.button("Afficher les statistiques"):
        from app.utils.api import get_statistics_by_genre_year
        try:
            data = get_statistics_by_genre_year(genre, year)

            if not data:
                st.warning("Aucune donnée trouvée pour cette combinaison genre/année.")
            else:
                # Afficher les meilleurs films
                top_films = data["top_films"]
                if top_films:
                    st.markdown(f"### 🎬 Top {len(top_films)} films {genre.title()} en {year}")
                    df = pd.DataFrame(top_films)
                    df = df.rename(columns={
                        "title": "Titre",
                        "release_date": "Date de sortie",
                        "vote_average": "Note moyenne"
                        })
                    df["Note moyenne"] = df["Note moyenne"].round(2)
                    st.dataframe(df)
                else:
                    st.info("Aucun film trouvé pour ce genre et cette année.")

                # Afficher les statistiques du genre
                genre_stats = data["genre_statistics"]
                st.markdown("### 📊 Statistiques du genre")
                st.write(f"Le genre **{genre.title()}** apparaît dans **{genre_stats['count']}** films en {year}.")
        except Exception as e:
            st.error(f"Erreur lors de la récupération des statistiques : {e}")
if section == "🎬 Détails d'un Film":
    st.subheader("Afficher un film en détails")
    film_id = st.number_input("ID du Film", min_value=1, step=1)
    
    if st.button("Afficher le Film"):
        afficher_film_complet(film_id)
