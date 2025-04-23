import requests
import os

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

