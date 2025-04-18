# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import duckdb
from collections import Counter
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date



# Pydantic models
class Film(BaseModel):
    film_id: int
    title: str
    genres: str
    description: str
    release_date: date
    vote_average: float
    vote_count: int

class FilmListResponse(BaseModel):
    films: List[Film]


class RecommendRequest(BaseModel):
    user_id: int
    num_recommendations: Optional[int] = 5

class Recommendation(BaseModel):
    movie_id: int
    predicted_rating: float

class RecommendResponse(BaseModel):
    user_id: int
    recommendations: List[Recommendation]

class TopFilm(BaseModel):
    title: str
    vote_average: float
    release_date: date
class ListTopFilm(BaseModel):
    top_films:List[TopFilm]
class GenreStatistics(BaseModel):
    genre: str
    count: int

class StatisticsResponse(BaseModel):
    top_films: List[TopFilm]
    genre_statistics: GenreStatistics

class GenreDistribution(BaseModel):
    genre: str
    count: int

class DistributionGenresResponse(BaseModel):
    year: int
    genres: List[GenreDistribution]


##Fastapi
app = FastAPI()

def get_db_connection():
    con = duckdb.connect("data/films_reco.db")
    try:
        yield con
    finally:
        con.close()

@app.post("/recommendations/{user_id}")
def get_recommendations(user_id: int,con: duckdb.DuckDBPyConnection = Depends(get_db_connection)):
    result = con.execute("SELECT * FROM ratings").fetchall()[0:10] 
    
@router.get("/recommend/{user_id}", response_model=RecommendResponse)
def recommend(user_id: int, num_recommendations: int = 5):
    recommendations = get_recommendations(user_id, num_recommendations)
    return {"user_id": user_id, "recommendations": recommendations}

@app.get("/")
def root_api():
    return {"message": "API de recommandation de films"}

# Route pour récupérer tous les films
@app.get("/films",response_model=FilmListResponse)
def get_films(con: duckdb.DuckDBPyConnection = Depends(get_db_connection)):
    result = con.execute("SELECT * FROM films").fetchall()[0:10] 

    # Vérifier si des films ont été trouvés
    if not result:
        raise HTTPException(status_code=404, detail="Aucun film trouvé.")
    
    films = [
        Film(
            film_id=row[0],
            title=row[1],
            genres=row[2],
            description=row[3],
            release_date=row[4],
            vote_average=row[5],
            vote_count=row[6]
        )
        for row in result
    ]
    return FilmListResponse(films=films)

# Route pour récupérer un film par son ID
@app.get("/films/{id}",response_model=Film)
def get_film_by_id(id: int, con: duckdb.DuckDBPyConnection = Depends(get_db_connection)):
    query = "SELECT * FROM films WHERE id = ?"
    row = con.execute(query, [id]).fetchone()
    return Film(
            film_id=row[0],
            title=row[1],
            genres=row[2],
            description=row[3],
            release_date=row[4],
            vote_average=row[5],
            vote_count=row[6]
        )



def count_genres(genre_rows: list[str]) -> Counter:
    genre_counter = Counter()

    for genre_str in genre_rows:
        #print(f"Processing genre string: {genre_str}")
        if not genre_str:
            continue
        genres = genre_str.split(",")
        for g in genres:
            g = g.strip()
            if g:
                genre_counter[g] += 1

    print(f"Final genre counts: {genre_counter}")
    return genre_counter

@app.get("/statistics/distribution_genres/{year}", response_model=DistributionGenresResponse)
def distribution_genres(year: int, con: duckdb.DuckDBPyConnection = Depends(get_db_connection)):
    # Query to get all genres for the given year
    genre_query = """
    SELECT genres
    FROM films
    WHERE STRFTIME('%Y', release_date) = ?
    """
    rows = con.execute(genre_query, [str(year)]).fetchall()
    # Extraire seulement les chaînes non vides
    genre_strings = [row[0] for row in rows if row[0]]
    if not genre_strings:
        raise HTTPException(status_code=404, detail="No genre data found for the given year.")

    # Utiliser la fonction utilitaire
    genre_counter = count_genres(genre_strings)

    # Sort the genres
    sorted_genres = sorted(genre_counter.items(), key=lambda x: x[1], reverse=True)
    result = [GenreDistribution(genre=genre, count=count) for genre, count in sorted_genres]

    return DistributionGenresResponse(year=year, genres=result)


@app.get("/statistics/{year}",response_model=ListTopFilm)  # Global
def get_top10_film(year: int,con: duckdb.DuckDBPyConnection = Depends(get_db_connection)):
    # Query to get the top 10 films by average vote for the given year and genre
    top_films_query = """
    SELECT title, vote_average, release_date
    FROM films
    WHERE STRFTIME('%Y', release_date) = ?
    ORDER BY vote_average DESC
    LIMIT 10
    """
    top_films = con.execute(top_films_query, [str(year)]).fetchall()
    # If no top films found, return a message
    if not top_films:
        raise HTTPException(status_code=404, detail="No films found for the given year.")
    top_films_response = [TopFilm(title=film[0],vote_average=film[1],release_date=film[2]) for film in top_films]
    return ListTopFilm(top_films=top_films_response)

@app.get("/statistics/{gender}/{year}", response_model=StatisticsResponse)
def get_statistics(gender: str, year: int,con: duckdb.DuckDBPyConnection = Depends(get_db_connection)):
    # Query to get the top 10 films by average vote for the given year and genre
    top_films_query = """
    SELECT title, vote_average, release_date
    FROM films
    WHERE STRFTIME('%Y', release_date) = ? AND genres LIKE ?
    ORDER BY vote_average DESC
    LIMIT 10
    """
    top_films = con.execute(top_films_query, [str(year),f'%{gender}%']).fetchall()

    # If no top films found, return a message
    if not top_films:
        raise HTTPException(status_code=404, detail="No films found for the given year.")

    # Query genre  count for for the given year
    genre_stats_query = """
    SELECT genres
    FROM films
    WHERE STRFTIME('%Y', release_date) = ? AND genres LIKE ?
    """
    genre_stats = con.execute(genre_stats_query, [str(year), f'%{gender}%']).fetchall()
    genre_strings = [row[0] for row in genre_stats if row[0]]
    # Utiliser la fonction utilitaire
    genre_counter = count_genres(genre_strings)
    # print([film for film in top_films])
    # print(genre_counter[f'{gender}'])

    top_films_response = [TopFilm(title=film[0],vote_average=film[1],release_date=film[2]) for film in top_films]
    genre_stats_response = GenreStatistics(genre=gender, count=genre_counter[f'{gender}'])

    return StatisticsResponse(top_films=top_films_response,genre_statistics=genre_stats_response)




