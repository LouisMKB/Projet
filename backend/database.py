# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Remplace par le chemin de ta base de données existante
DATABASE_URL = "duckdb:///path/to/your/database.duckdb"  # Utilise le chemin vers ta base existante

# Créer l'engine de connexion DuckDB
engine = create_engine(DATABASE_URL, echo=True)

# Session local pour exécuter des requêtes
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

print(2)