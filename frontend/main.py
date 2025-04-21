import streamlit as st
from app.utils.api import get_all_movies, get_user_recommendations
from app.utils.charts import (
    plot_rating_distribution,
    plot_movies_per_year,
    plot_top_movies
)

st.set_page_config(
    page_title="Film Recommender Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("🎬 Film Recommender")
section = st.sidebar.radio("Navigation", [
    "📊 Statistiques des films",
    "🎯 Recommandations personnalisées"
])

st.title("🎥 Tableau de bord de recommandations de films")

if section == "📊 Statistiques des films":
    # Choix de la page pour charger les films
    page_num = st.sidebar.number_input(
        "Page des films à charger", min_value=1, max_value=100, value=1
    )
    st.subheader(f"Chargement des films - Page {page_num}")
    movies = get_all_movies(page=page_num)


def fetch_films():
    try:
        response = requests.get(f"{backend_url}/films")
        return response.json().get('films', []) if response.status_code == 200 else {"error": "Erreur films."}
    except Exception as e:
        return {"error": str(e)}

def fetch_recommendations(user_id):
    try:
        response = requests.post(f"{backend_url}/recommendation_movies/{user_id}")
        return response.json() if response.status_code == 200 else {"error": "Erreur recommandations."}
    except Exception as e:
        return {"error": str(e)}

st.title("🎬 Tableau de bord des films")

# Accueil
greeting = fetch_greeting()
if 'error' in greeting:
    st.error(greeting['error'])
else:
    st.success(greeting.get("message", "Bienvenue !"))

# Affichage des films
st.header("📽️ Liste des films")
films = fetch_films()
if isinstance(films, list):
    for film in films:
        st.subheader(film['title'])
        st.write(f"Genres: {film['genres']}")
        st.write(f"Description: {film['description']}")
        st.write(f"Sortie: {film['release_date']}")
        st.write(f"Note moyenne: {film['vote_average']}")
        st.markdown("---")
else:
    st.error("Erreur lors du chargement des films.")

# Recommandations
st.header("🎯 Recommandations personnalisées")
user_id = st.text_input("Entrez votre ID utilisateur :", value="1")
if st.button("Obtenir recommandations"):
    recos = fetch_recommendations(user_id)
    if 'error' in recos:
        st.error(recos['error'])
    else:
        for film in recos["recommendations"]:
            st.subheader(film['title'])
            st.write(f"film_id:{film['movie_id']}")
            st.write(f"Note prédite: {film['rating_predicted']:.2f}/5")
            st.markdown("---")

    if not movies:
        st.error("Impossible de récupérer les films pour cette page.")
    else:
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
            recommendations = get_user_recommendations(user_id, num_reco)
            if recommendations:
                st.success(f"Voici {len(recommendations)} recommandations pour l'utilisateur {user_id}:")
                cols = st.columns(5)
                for i, film in enumerate(recommendations):
                    with cols[i % 5]:
                        # Affiche l'affiche si disponible
                        poster = film.get('poster_path')
                        if poster:
                            st.image(poster, width=120)
                        st.caption(film.get('title', 'Titre inconnu'))
            else:
                st.warning("Aucune recommandation trouvée pour cet utilisateur.")
        except Exception as e:
            st.error(f"Erreur lors de la récupération des recommandations : {e}")
