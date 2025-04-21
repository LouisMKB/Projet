import streamlit as st
import requests
import os
import pandas as pd

from pathlib import Path


backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

def fetch_greeting():
    try:
        response = requests.get(f"{backend_url}/")
        return response.json() if response.status_code == 200 else {"error": "Erreur lors de la récupération."}
    except Exception as e:
        return {"error": str(e)}

def fetch_films():
    try:
        response = requests.get(f"{backend_url}/films")
        return response.json().get('films', []) if response.status_code == 200 else {"error": "Erreur films."}
    except Exception as e:
        return {"error": str(e)}

def fetch_recommendations(user_id):
    try:
        response = requests.post(f"{backend_url}/recommendations/{user_id}")
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
        for film in recos:
            st.subheader(film['title'])
            st.write(f"Genres: {film['genres']}")
            st.write(f"Note prédite: {film['rating_predicted']:.2f}/5")
            st.markdown("---")

# Statistiques

st.header("📊 Statistiques")
try:
    ratings_path = Path(__file__).resolve().parents[2] / "backend" /"app"/"utils"/ "data" / "ratings.csv"
    stats_df = pd.read_csv(ratings_path)
    avg_rating = stats_df.groupby("userId")["rating"].mean().sort_values(ascending=False)
    st.bar_chart(avg_rating)
except Exception as e:
    st.error(f"Erreur chargement stats: {e}")
