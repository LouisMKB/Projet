import requests
import os

backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

def fetch_greeting():
    return requests.get(f"{backend_url}/").json()

def fetch_films():
    return requests.get(f"{backend_url}/films").json()

def fetch_recommendations(user_id):
    return requests.post(f"{backend_url}/recommendations/{user_id}").json()
