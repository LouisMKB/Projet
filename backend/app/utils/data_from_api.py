import requests
import json
import os
import time
from dotenv import load_dotenv

# Charger le fichier .env
load_dotenv()

def load_movie_metadata():
    api_key = os.getenv("TMDB_API_KEY")
    if api_key is None:
        print("Erreur : clé API non trouvée.")
        return

    base_url = "https://api.themoviedb.org/3/movie/popular"
    headers = {"Accept": "application/json"}

    all_movies = []
    page = 1
    max_pages =1000  # Limite imposée par l'API TMDb

    while page <= max_pages:
        print(f"Chargement de la page {page}...")
        url = f"{base_url}?api_key={api_key}&language=en-US&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            movies = data.get("results", [])
            if not movies:
                print("Plus de résultats.")
                break
            all_movies.extend(movies)
            page += 1
            time.sleep(0.2)  # Petite pause pour éviter le rate limit
        else:
            print(f" Erreur HTTP ({response.status_code}) sur la page {page}.")
            break

    # Enregistrement dans un fichier JSON
    with open("data/movies_database.json", "w", encoding="utf-8") as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=4)

    print(f"{len(all_movies)} films enregistrés dans 'movies_database.json'.")

def load_genres():
    
    api_key = os.getenv("TMDB_API_KEY")
    if api_key is None:
        print("Erreur : clé API non trouvée.")
        return

    base_url= "https://api.themoviedb.org/3/genre/movie/list"
    url=f"{base_url}?api_key={api_key}&language=en"
    headers = {"Accept": "application/json"}
    response=requests.get(url,headers=headers)
    data=[]
    data=response.json()

    
    with open("data/movies_genre.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Lancer l’import
if __name__ == "__main__":
    load_movie_metadata()
    load_genres()
