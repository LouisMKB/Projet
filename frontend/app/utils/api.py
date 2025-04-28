import requests
import os
import streamlit as st
from datetime import datetime
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")



def get_all_movies(page: int = 1):
    """
    Renvoie la liste de films (clé 'films') depuis l'endpoint paginé /films?page=...
    """
    try:
        resp = requests.get(f"{BACKEND_URL}/films?page={page}")
        resp.raise_for_status()
        data = resp.json()
        return data.get("films", [])   # <— on extrait la liste ici
    except Exception as e:
        print(f"Erreur lors de get_all_movies: {e}")
        return []

def get_movie_by_id(movie_id: int):
    response = requests.get(f"{BACKEND_URL}/films/{movie_id}")
    return response.json() if response.status_code == 200 else None

def get_user_recommendations(user_id: int, num_recommendations: int = 5):
    params = {"num_recommendations": num_recommendations}
    response = requests.post(f"{BACKEND_URL}/recommendation_movies/{user_id}", params=params)
    return response.json() if response.status_code == 200 else []

def get_statistics_by_genre_year(genre: str, year: int):
    response = requests.get(f"{BACKEND_URL}/statistics/{genre}/{year}")
    return response.json() if response.status_code == 200 else None

def afficher_film_complet(film_id: int):
    # Si tu as déjà un film en JSON (ex : récupéré depuis ton backend ou un fichier)
    film_data = get_movie_by_id(film_id)  # Cette fonction doit te renvoyer le film au format dict
    
    if not film_data:
        st.error("Film introuvable.")
        return

    # Extraire les informations du film
    title = film_data.get("title")
    release_date = film_data.get("release_date")
    overview = film_data.get("description", "Aucune description disponible.")
    vote_average = film_data.get("vote_average")
    poster_path = film_data.get("poster_path")
    genres = film_data.get("genres", "")  # Genres sous forme de texte
    vote_count = film_data.get("vote_count")

    # Créer deux colonnes : une pour l'affiche et l'autre pour le résumé
    col1, col2 = st.columns([1, 2])  # La colonne de gauche (col1) prendra moins d'espace que celle de droite (col2)
    
    # Affichage du poster dans la première colonne
    with col1:
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"  # URL complète pour l'image
            st.image(poster_url, width=300)  # Affiche l'image avec l'URL complète
    
    # Affichage du résumé et des informations dans la deuxième colonne
    with col2:
        # Titre et Date
        st.title(title)
        release_date_formatted = datetime.strptime(release_date, '%Y-%m-%d').strftime('%d %B %Y')  # Formatage de la date
        st.subheader(f"Date de sortie: {release_date_formatted}")
        st.write(f"#### Genres : {genres}")
    
    # Description du film
        st.write("#### Résumé (en anglais)")
        st.write(overview)
    
    # Note
    st.write(f"#### Note moyenne : {vote_average:.2f} / 10")
    st.write(f"#### Nombre de votes : {vote_count}")

    



