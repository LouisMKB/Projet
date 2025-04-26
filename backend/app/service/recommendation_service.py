import pandas as pd
import numpy as np
import duckdb
from ..models.schemas import RecommendResponse,Recommendation
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from typing import List
from pathlib import Path
from loguru import logger

def load_data():
    """
    Charge les données depuis la base DuckDB et construit la matrice utilisateur-film.

    :return: ratings_df, movies_df, ratings_matrix
    """
    try:
        films_path = Path(__file__).resolve().parents[2] / "app" / "utils" / "data" / "films_reco.db"
        with duckdb.connect(films_path) as conn:
            ratings_df = conn.execute("SELECT user_id, film_id, rating FROM ratings").df()
            movies_df = conn.execute("SELECT id AS film_id, title FROM films").df()
            ratings_df = ratings_df[ratings_df["film_id"].isin(movies_df["film_id"])]
            ratings_matrix = ratings_df.pivot_table(index='user_id', columns='film_id', values='rating').fillna(0)
        logger.info("Données chargées avec succès.")
        return ratings_df, movies_df, ratings_matrix
    except Exception as e:
        logger.error(f"Erreur lors du chargement des données : {e}")
        return None, None, None

def train_model(ratings_matrix, n_components=20):
    """
    Entraîne un modèle SVD et retourne les prédictions normalisées.

    :param ratings_matrix: matrice utilisateur-film
    :param n_components: nombre de composantes latentes
    :return: DataFrame des notes prédites
    """
    try:
        svd = TruncatedSVD(n_components=min(n_components, ratings_matrix.shape[1]-1), random_state=42)
        matrice_latente = svd.fit_transform(ratings_matrix)
        predicted_ratings = np.dot(matrice_latente, svd.components_)

        scaler = MinMaxScaler(feature_range=(0.5, 5))
        predicted_ratings_scaled = scaler.fit_transform(predicted_ratings)

        pred_df = pd.DataFrame(predicted_ratings_scaled, index=ratings_matrix.index, columns=ratings_matrix.columns)
        logger.info("Modèle entraîné avec succès.")
        return pred_df
    except Exception as e:
        logger.error(f"Erreur lors de l'entraînement du modèle : {e}")
        return None

def get_recommendation(user_id: int, ratings_df: pd.DataFrame, movies_df: pd.DataFrame, pred_df: pd.DataFrame, nombre_de_recommandation: int = 5) -> RecommendResponse:
    """
    Génère des recommandations de films pour un utilisateur donné.

    :param user_id: identifiant de l'utilisateur
    :param ratings_df: DataFrame des notes
    :param movies_df: DataFrame des films
    :param pred_df: Prédictions du modèle
    :param nombre_de_recommandation: nombre de films à recommander
    :return: RecommendResponse contenant la liste des recommandations
    """
    try:
        if pred_df is None or user_id not in pred_df.index:
            logger.warning(f"Utilisateur {user_id} introuvable dans les prédictions.")
            return RecommendResponse(user_id=user_id, recommendations=[])

        predictions = pred_df.loc[user_id]
        films_deja_notes = ratings_df[ratings_df['user_id'] == user_id]['film_id'].tolist()
        vrai_predictions = predictions.drop(index=films_deja_notes, errors='ignore')

        if vrai_predictions.empty:
            logger.info(f"Aucune recommandation disponible pour l'utilisateur {user_id}.")
            return RecommendResponse(user_id=user_id, recommendations=[])

        top_films = vrai_predictions.sort_values(ascending=False).head(nombre_de_recommandation)
        reco_df = pd.DataFrame({
            'film_id': top_films.index,
            'rating_predicted': top_films.values
        })

        reco_df['film_id'] = reco_df['film_id'].astype(int)
        reco_df2 = reco_df.merge(movies_df, on='film_id', how='left')
        reco_df2 = reco_df2.rename(columns={'film_id': 'movie_id'})

        recommandations: List[Recommendation] = [
            Recommendation(
                movie_id=row['movie_id'],
                title=row['title'],
                rating_predicted=row['rating_predicted']
            )
            for _, row in reco_df2.iterrows()
        ]

        logger.info(f"{len(recommandations)} recommandations générées pour l'utilisateur {user_id}.")
        return RecommendResponse(user_id=user_id, recommendations=recommandations)
    except Exception as e:
        logger.error(f"Erreur lors de la génération des recommandations pour l'utilisateur {user_id} : {e}")
        return RecommendResponse(user_id=user_id, recommendations=[])

def recommend_movies(user_id: int, nombre_de_recommandation: int = 10) -> RecommendResponse:
    """
    Point d'entrée principal pour générer des recommandations pour un utilisateur.

    :param user_id: identifiant utilisateur
    :param nombre_de_recommandation: nombre de recommandations souhaitées
    :return: RecommendResponse
    """
    try:
        ratings_df, movies_df, ratings_matrix = load_data()
        if ratings_df is None or ratings_matrix is None:
            return RecommendResponse(user_id=user_id, recommendations=[])
        pred_df = train_model(ratings_matrix)
        return get_recommendation(user_id, ratings_df, movies_df, pred_df, nombre_de_recommandation)
    except Exception as e:
        logger.error(f"Erreur dans recommend_movies pour l'utilisateur {user_id} : {e}")
        return RecommendResponse(user_id=user_id, recommendations=[])

def evaluate_model(ratings_matrix, n_components=20):
    """
    Évalue le modèle SVD avec les métriques RMSE et MAE.

    :param ratings_matrix: matrice utilisateur-film
    :param n_components: dimensions latentes
    :return: tuple (rmse, mae)
    """
    try:
        train_matrix, test_matrix = train_test_split(ratings_matrix, test_size=0.2, random_state=42)
        model = TruncatedSVD(n_components=n_components, random_state=42)
        model.fit(train_matrix)
        predicted_matrix = np.dot(model.transform(train_matrix), model.components_)

        test_values = test_matrix.values
        mask = test_values != 0

        true_ratings = test_values[mask]
        predicted_ratings = predicted_matrix[mask]

        rmse = np.sqrt(mean_squared_error(true_ratings, predicted_ratings))
        mae = mean_absolute_error(true_ratings, predicted_ratings)

        logger.info(f"Évaluation du modèle : RMSE={rmse:.4f}, MAE={mae:.4f}")
        return rmse, mae
    except Exception as e:
        logger.error(f"Erreur lors de l'évaluation du modèle : {e}")
        return None, None
