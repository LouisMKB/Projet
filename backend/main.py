from fastapi import FastAPI

app = FastAPI(title="Movie Recommendation API", version="1.0.0")

@app.get("/")
def ef read_root():
    return {"message": "Bienvenue sur l'API de recommandation de films !"}


