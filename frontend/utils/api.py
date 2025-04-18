import requests
import pandas as pd

BACKEND_URL = "http://backend:8000"  # ou http://localhost:8000 si local

def get_recommendations(user_id):
    response = requests.post(f"{BACKEND_URL}/recommendations/{user_id}")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    return pd.DataFrame()

def get_user_ratings(user_id):
    # À adapter selon l’API backend (ou lecture locale si nécessaire)
    return pd.DataFrame([
        {"film_id": 1, "rating": 4.5},
        {"film_id": 2, "rating": 3.0}
    ])
