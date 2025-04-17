# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import duckdb
from collections import Counter


app = FastAPI()

@app.get("/")
def root_api():
    return {"message": "API de recommandation de films"}

# Route pour récupérer tous les films
@app.get("/films")
def get_films():
    con = duckdb.connect("data/films_reco.db")
    result = con.execute("SELECT * FROM films").fetchall()[0:10] # Utilise le nom de ta table "films"
    return [{"film_id": row[0],
            "title": row[1],
            "genres": row[2],
            "description": row[3],
            "release_date": row[4],
            "vote_average": row[5],
            "vote_count": row[6]} for row in result]


# Route pour récupérer un film par son ID
@app.get("/films/{id}")
def get_film_by_id(id: int):
    con = duckdb.connect("data/films_reco.db")
    query = "SELECT * FROM films WHERE id = ?"
    result = con.execute(query, [id]).fetchone()
    con.close()
    return {
        "film_id": result[0],
        "title": result[1],
        "genres": result[2],
        "description": result[3],
        "release_date": result[4],
        "vote_average": result[5],
        "vote_count": result[6]
    }

@app.post("/recommendations/{user_id}")
def get_recommendations(user_id: int):
    con = duckdb.connect("data/films_reco.db")

@app.get("/statistics/{gender}/{year}")
def get_statistics(gender: str, year: int):
    con = duckdb.connect("data/films_reco.db")
    
    # Requête pour le top 10 des films par note moyenne pour l'année donnée
    top_films_query = """
    SELECT title, vote_average, release_date
    FROM films
    WHERE STRFTIME('%Y', release_date) = ?
    ORDER BY vote_average DESC
    LIMIT 10
    """
    top_films = con.execute(top_films_query, [str(year)]).fetchall()


    # Requête pour la répartition des films par genre pour l'année donnée
    genre_stats_query = """
    SELECT genres, COUNT(*) AS genre_count
    FROM films
    WHERE STRFTIME('%Y', release_date) = ? AND genres LIKE ?
    GROUP BY genres
    ORDER BY genre_count DESC
    """
    genre_stats = con.execute(genre_stats_query, [str(year), f'%{gender}%']).fetchall()

    return {
        "top_films": [
            {"title": film[0], "vote_average": film[1], "release_date": film[2]}
            for film in top_films
        ],
        "genre_statistics": [
            {"genre": stat[0], "count": stat[1]} for stat in genre_stats
        ]
    }


def get_db_connection():
    con = duckdb.connect("data/films_reco.db")
    try:
        yield con
    finally:
        con.close()

@app.get("/special/distribution_genres/{year}")
def distribution_genres(year: int,con: duckdb.DuckDBPyConnection = Depends(get_db_connection)):
    # Récupère tous les genres pour l'année donnée
    genre_query = """
    SELECT genres
    FROM films
    WHERE STRFTIME('%Y', release_date) = ?
    """
    rows = con.execute(genre_query, [str(year)]).fetchall()
    con.close()
    
    genre_counter = Counter()

    for row in rows:
        if not row[0]:  # ignore les champs vides ou None
            continue
        genres = row[0].split(",")
        for g in genres:
            g = g.strip()
            genre_counter[g] += 1

    # Résultat trié
    sorted_genres = sorted(genre_counter.items(), key=lambda x: x[1], reverse=True)
    result = [{"genre": genre, "count": count} for genre, count in sorted_genres]

    return {"year": year, "genres": result}

