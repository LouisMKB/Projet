# main.py
from fastapi import FastAPI
from backend.app.routers.recommender import router


##Fastapi
app = FastAPI()



# Inclure les routeurs
app.include_router(router, tags=["recommender"])


@app.get("/")
def read_root_api():
    return {"message": "Bienvenue sur l'API de recommandation de films !"}

