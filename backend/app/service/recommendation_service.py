import pandas as pd
import numpy as np
import duckdb
from backend.app.models.schemas import RecommendResponse,Recommendation
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MinMaxScaler
from typing import List

def load_data():
    with duckdb.connect("data/films_reco.db") as conn:
        ratings_df = conn.execute("SELECT user_id, film_id, rating FROM ratings").df()
        movies_df = conn.execute("SELECT id AS film_id, title FROM films").df()
        ratings_df = ratings_df[ratings_df["film_id"].isin(movies_df["film_id"])]
        ratings_matrix = ratings_df.pivot_table(index='user_id', columns='film_id', values='rating').fillna(0)
    return ratings_df, movies_df, ratings_matrix


def train_model(ratings_matrix, n_components=20):
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    matrice_latente = svd.fit_transform(ratings_matrix)
    U_sig = matrice_latente
    V_trans = svd.components_
    predicted_ratings = np.dot(U_sig, V_trans)

    scaler = MinMaxScaler(feature_range=(0.5, 5))
    predicted_ratings_scaled = scaler.fit_transform(predicted_ratings)

    pred_df = pd.DataFrame(predicted_ratings_scaled, index=ratings_matrix.index, columns=ratings_matrix.columns)
    return pred_df



def get_recommendation(user_id: int, ratings_df: pd.DataFrame, movies_df: pd.DataFrame, pred_df: pd.DataFrame, nombre_de_recommandation: int = 5) -> RecommendResponse:
    if user_id not in pred_df.index:
        print(f"L'utilisateur {user_id} n'existe pas dans les prédictions.")
        return RecommendResponse(user_id=user_id, recommendations=[])
    predictions = pred_df.loc[user_id]
    films_deja_notes = ratings_df[ratings_df['user_id'] == user_id]['film_id'].tolist()
    vrai_predictions = predictions.drop(index=films_deja_notes)

    if vrai_predictions.empty:
        print(f"Aucune recommandation disponible pour l'utilisateur {user_id}.")
        return RecommendResponse(user_id=user_id, recommendations=[])

    top_films = vrai_predictions.sort_values(ascending=False).head(nombre_de_recommandation)
    reco_df = pd.DataFrame({
        'film_id': top_films.index,
        'rating_predicted': top_films.values
    })

    reco_df['film_id'] = reco_df['film_id'].astype(int)
    reco_df2 = reco_df.merge(movies_df, left_on='film_id', right_on='film_id', how='left')
    reco_df2 = reco_df2.rename(columns={'film_id': 'movie_id'})

    recommandations: List[Recommendation] = [
        Recommendation(
            movie_id=row['movie_id'],
            title=row['title'],
            rating_predicted=row['rating_predicted']
        )
        for _, row in reco_df2.iterrows()
    ]

    return RecommendResponse(user_id=user_id,recommendations=recommandations)

def recommend_movies(user_id: int, nombre_de_recommandation: int = 10) -> RecommendResponse:
    ratings_df, movies_df, ratings_matrix = load_data()
    pred_df = train_model(ratings_matrix)
    return get_recommendation(user_id, ratings_df, movies_df, pred_df, nombre_de_recommandation)

