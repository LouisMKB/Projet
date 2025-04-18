from surprise import Dataset, Reader, SVD
import pandas as pd
import duckdb

# Connexion DuckDB (tu peux remplacer par un Depends si tu veux l'intégrer à FastAPI)
def get_duckdb_connection():
    return duckdb.connect("data/films.db")  # Change le chemin si besoin

# Charger les données depuis DuckDB
def load_data_from_duckdb():
    con = get_duckdb_connection()
    query = "SELECT user_id, item_id, rating FROM ratings"
    df = con.execute(query).fetchdf()
    
    reader = Reader(rating_scale=(1, 5))
    dataset = Dataset.load_from_df(df[['user_id', 'item_id', 'rating']], reader)
    return dataset

# Modèle global
model = SVD()

# Entraînement
def train_model():
    dataset = load_data_from_duckdb()
    trainset = dataset.build_full_trainset()
    model.fit(trainset)
    return {"message": "Modèle entraîné avec succès !"}

# Recommandations pour un utilisateur
def get_recommendations(user_id: int, num_recommendations: int = 5):
    dataset = load_data_from_duckdb()
    trainset = dataset.build_full_trainset()
    testset = trainset.build_anti_testset()

    predictions = model.test(testset)

    user_recs = [
        {"movie_id": int(pred.iid), "predicted_rating": pred.est}
        for pred in predictions if int(pred.uid) == user_id
    ]

    user_recs.sort(key=lambda x: x["predicted_rating"], reverse=True)
    return user_recs[:num_recommendations]
