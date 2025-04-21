import pandas as pd
import numpy as np
import duckdb
from loguru import logger
from ..models.schemas import RecommendResponse, Recommendation
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from typing import List

logger = logging.getLogger(__name__)

def load_data():
    """
    Charge les données de notation et de films depuis une base DuckDB.
    Crée une matrice utilisateur-film pour l'entraînement.

    :return: ratings_df, movies_df, ratings_matrix
    """
    try:
        with duckdb.connect("data/films_reco.db") as conn:
            ratings_df = conn.execute("SELECT user_id, film_id, rating FROM ratings").df()
            movies_df = conn.execute("SELECT id AS film_id, title FROM films").df()
            ratings_df = ratings_df[ratings_df["film_id"].isin(movies_df["film_id"])]
            ratings_matrix = ratings_df.pivot_table(index='user_id', columns='film_id', values='rating').fillna(0)
        return ratings_df, movies_df, ratings_matrix
    except Exception as e:
        logger.exception("Erreur lors du chargement des données")
        raise


def train_model(ratings_matrix, n_components=20):
    """
    Entraîne un modèle SVD sur la matrice utilisateur-film et retourne les prédictions.

    :param ratings_matrix: matrice utilisateur-film
    :param n_components: nombre de composantes latentes
    :return: DataFrame des notes prédites
    """
    try:
        svd = TruncatedSVD(n_components=n_components, random_state=42)
        matrice_latente = svd.fit_transform(ratings_matrix)
        U_sig = matrice_latente
        V_trans = svd.components_
        predicted_ratings = np.dot(U_sig, V_trans)

        scaler = MinMaxScaler(feature_range=(0.5, 5))
        predicted_ratings_scaled = scaler.fit_transform(predicted_ratings)

        pred_df = pd.DataFrame(predicted_ratings_scaled, index=ratings_matrix.index, columns=ratings_matrix.columns)
        return pred_df
    except Exception as e:
        logger.exception("Erreur lors de l'entraînement du modèle SVD")
        raise


def get_recommendation(user_id: int, ratings_df: pd.DataFrame, movies_df: pd.DataFrame, pred_df: pd.DataFrame, nombre_de_recommandation: int = 5) -> RecommendResponse:
    """
    Génére une liste de recommandations pour un utilisateur donné.

    :param user_id: ID de l'utilisateur
    :param ratings_df: DataFrame des notes
    :param movies_df: DataFrame des films
    :param pred_df: Prédictions générées par le modèle
    :param nombre_de_recommandation: nombre de recommandations à retourner
    :return: RecommendResponse contenant les films recommandés
    """
    try:
        if user_id not in pred_df.index:
            logger.warning(f"L'utilisateur {user_id} n'existe pas dans les prédictions.")
            return RecommendResponse(user_id=user_id, recommendations=[])

        predictions = pred_df.loc[user_id]
        films_deja_notes = ratings_df[ratings_df['user_id'] == user_id]['film_id'].tolist()
        vrai_predictions = predictions.drop(index=films_deja_notes)

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

        return RecommendResponse(user_id=user_id, recommendations=recommandations)
    except Exception as e:
        logger.exception(f"Erreur lors de la génération des recommandations pour l'utilisateur {user_id}")
        raise


def recommend_movies(user_id: int, nombre_de_recommandation: int = 10) -> RecommendResponse:
    """
    Fonction principale pour obtenir des recommandations de films pour un utilisateur donné.

    :param user_id: ID de l'utilisateur
    :param nombre_de_recommandation: nombre de recommandations à retourner
    :return: RecommendResponse contenant les recommandations
    """
    try:
        ratings_df, movies_df, ratings_matrix = load_data()
        pred_df = train_model(ratings_matrix)
        return get_recommendation(user_id, ratings_df, movies_df, pred_df, nombre_de_recommandation)
    except Exception as e:
        logger.exception(f"Erreur lors de la recommandation pour l'utilisateur {user_id}")
        return RecommendResponse(user_id=user_id, recommendations=[])


def evaluate_model(ratings_matrix, n_components=20):
    """
    Évalue le modèle SVD en utilisant RMSE et MAE sur un sous-ensemble test.

    :param ratings_matrix: matrice utilisateur-film
    :param n_components: nombre de composantes latentes
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

        return rmse, mae
    except Exception as e:
        logger.exception("Erreur lors de l'évaluation du modèle SVD")
        raise
