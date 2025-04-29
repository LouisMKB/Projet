import requests
import json
import time
import logging
from dotenv import load_dotenv
import os

# Charger le .env pour récupérer TMDB_BEARER_TOKEN
load_dotenv()
logger = logging.getLogger(__name__)

TMDB_BEARER_TOKEN = os.getenv("TMDB_BEARER_TOKEN")
if not TMDB_BEARER_TOKEN:
    logger.error("❌ TMDB_BEARER_TOKEN non trouvé dans .env")
    exit(1)

HEADERS = {
    "Authorization": f"Bearer {TMDB_BEARER_TOKEN}",
    "Accept": "application/json"
}

#La fonction qui suit était utilisé de base mais pour arrivé à 10000 films on va utiliser toutes les tables avec la fonction juste après
def load_movie_metadata(max_pages: int = 5):
    """
    Récupère les films populaires depuis TMDB en utilisant le Bearer Token v4
    et écrit le résultat dans data/movies_database.json
    """
    base_url = "https://api.themoviedb.org/3/movie/popular"
    all_movies = []
    for page in range(1, max_pages + 1):
        logger.info(f"🔄 Chargement de la page {page}...")
        resp = requests.get(base_url, headers=HEADERS, params={"language": "en-US", "page": page})
        if resp.status_code != 200:
            logger.error(f"❌ Erreur HTTP {resp.status_code} sur TMDB page {page}")
            break
        data = resp.json().get("results", [])
        if not data:
            logger.info("⚠️ Plus de résultats disponibles.")
            break
        all_movies.extend(data)
        time.sleep(0.2)
    # Sauvegarde JSON
    os.makedirs("data", exist_ok=True)
    with open("backend/app/utils/data/movies_database.json", "w", encoding="utf-8") as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=4)
    logger.info(f"✅ {len(all_movies)} films enregistrés dans 'data/movies_database.json'.")


#Cette fonction quoique plus lente nous a permis d'avoir 10000 films en prenant vraiment toute les tables
def collect_unique_movies(target_count=10000):
    """
    Récupère des films depuis plusieurs endpoints de TMDB
    jusqu'à atteindre target_count films uniques.
    """
    endpoints = [
        "movie/popular",
        "movie/top_rated",
        "movie/now_playing",
        "movie/upcoming",
        "discover/movie"
    ]
    all_movies_dict = {}
    current_page = 1
    max_page_limit = 500  # TMDB limite à 500 pages max

    while len(all_movies_dict) < target_count:
        for endpoint in endpoints:
            if endpoint == "discover/movie":
                # Pour éviter de toujours avoir les mêmes films dans discover,
                # on utilise une page aléatoire
                page = (current_page % max_page_limit) + 1
            else:
                page = current_page

            logger.info(f"🔄 Chargement {endpoint}, page {page}...")

            resp = requests.get(
                f"https://api.themoviedb.org/3/{endpoint}",
                headers=HEADERS,
                params={"language": "en-US", "page": page}
            )

            if resp.status_code != 200:
                logger.warning(f"⚠️ Erreur HTTP {resp.status_code} pour {endpoint} page {page}")
                continue

            movies = resp.json().get("results", [])
            for movie in movies:
                movie_id = movie.get("id")
                if movie_id and movie_id not in all_movies_dict:
                    all_movies_dict[movie_id] = movie
                    if len(all_movies_dict) >= target_count:
                        break

            time.sleep(0.2)

            if len(all_movies_dict) >= target_count:
                break

        current_page += 1

    logger.info(f"✅ {len(all_movies_dict)} films uniques collectés.")

    # Sauvegarde
    os.makedirs("backend/app/utils/data", exist_ok=True)
    with open("backend/app/utils/data/movies_database.json", "w", encoding="utf-8") as f:
        json.dump(list(all_movies_dict.values()), f, ensure_ascii=False, indent=4)

    logger.info("🎉 Fichier JSON mis à jour avec 10 000 films uniques.")


def load_genres():
    """
    Récupère la liste des genres depuis TMDB et l'écrit dans data/movies_genre.json
    """
    url = "https://api.themoviedb.org/3/genre/movie/list"
    logger.info("🔄 Chargement des genres TMDB...")
    resp = requests.get(url, headers=HEADERS, params={"language": "en-US"})
    if resp.status_code != 200:
        logger.error(f"❌ Erreur HTTP {resp.status_code} lors de la récupération des genres")
        return
    data = resp.json().get("genres", [])
    os.makedirs("data", exist_ok=True)
    with open("backend/app/utils/data/movies_genre.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info(f"✅ {len(data)} genres enregistrés dans 'data/movies_genre.json'.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    #load_movie_metadata(max_pages=500)
    collect_unique_movies(target_count=10000)
    load_genres()
