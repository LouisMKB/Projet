# main.py
from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from app.routers.recommender import router
##Fastapi
app = FastAPI()

# Inclure les routeurs
app.include_router(router, tags=["recommender"])


@app.get("/")
def read_root_api():
    return {"message": "Bienvenue sur l'API de recommandation de films!"}
 
