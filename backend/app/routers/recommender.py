from fastapi import APIRouter, HTTPException,Depends,Query
from collections import Counter
from ..service.recommendation_service import recommend_movies
from ..models.schemas import( Film,FilmListResponse,RecommendRequest,Recommendation,
RecommendResponse,TopFilm,ListTopFilm,StatisticsResponse,GenreStatistics,DistributionGenresResponse,GenreDistribution)
import duckdb
from app.utils.count_gender import count_gender
router = APIRouter()


def get_db_connection():
    con = duckdb.connect("data/films_reco.db")
    try:
        yield con
    finally:
        con.close()
        

# Route pour récupérer tous les films
@router.get("/films",response_model=FilmListResponse)
def get_films(page: int = Query(1, ge=1,le=500),con: duckdb.DuckDBPyConnection = Depends(get_db_connection)):
    """Affiche 20 films par page"""
    films_per_page = 20
    offset = (page - 1) * films_per_page
    result = con.execute(f"SELECT * FROM films LIMIT {films_per_page} OFFSET {offset}").fetchall()

    # Vérifier si des films ont été trouvés
    if not result:
        raise HTTPException(status_code=404, detail="Aucun film trouvé pour cette page.")
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
@router.get("/films/{id}",response_model=Film)
def get_film_by_id(id: int, con: duckdb.DuckDBPyConnection = Depends(get_db_connection)):
    """
    Renvoie les détails d'un film, lorsqu'on fournit son identifiant
    """
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


@router.post("/recommendation_movies/{user_id}", response_model=RecommendResponse)
def get_recommendations(user_id:int,num_recommendations:int=5):
    """
    Endpoint pour obtenir des recommandations de films pour un utilisateur spécifié
    - user_id: Identifiant de l'utilisateur
    - nombre_de_recommandation: Nombre de recommandations à retourner
    """
    return recommend_movies(user_id,num_recommendations)
    


@router.get("/statistics/{year}",response_model=ListTopFilm)  # Global
def get_top10_film(year: int,con: duckdb.DuckDBPyConnection = Depends(get_db_connection)):
    """ 
    Query to get the top 10 films by average vote for the given year
    """
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




@router.get("/statistics/distribution_genres/{year}", response_model=DistributionGenresResponse)
def distribution_genres(year: int, con: duckdb.DuckDBPyConnection = Depends(get_db_connection)):
    """ 
    The query gives  the distributions count of genres for the given year
    """
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
    genre_counter = count_gender(genre_strings)

    # Sort the genres
    sorted_genres = sorted(genre_counter.items(), key=lambda x: x[1], reverse=True)
    result = [GenreDistribution(genre=genre, count=count) for genre, count in sorted_genres]

    return DistributionGenresResponse(year=year, genres=result)




@router.get("/statistics/{gender}/{year}", response_model=StatisticsResponse)
def get_statistics(gender: str, year: int,con: duckdb.DuckDBPyConnection = Depends(get_db_connection)):
    """Query to get the top 10 films by average vote for the given year and genre.
    Gives also the number of film of this genre the year chosen
    """
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
    genre_counter = count_gender(genre_strings)
    # print([film for film in top_films])
    # print(genre_counter[f'{gender}'])

    top_films_response = [TopFilm(title=film[0],vote_average=film[1],release_date=film[2]) for film in top_films]
    genre_stats_response = GenreStatistics(genre=gender, count=genre_counter[f'{gender}'])

    return StatisticsResponse(top_films=top_films_response,genre_statistics=genre_stats_response)
