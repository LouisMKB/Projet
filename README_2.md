# Projet sur la recommendation de films

## NOM Prénom :

KOUMBA BOUNDA Louis-Marie
LECLERC Cédric

### **Pour rappel voici le contexte du projet :** 
En tant que plateforme de streaming de contenus audiovisuels, nous souhaitons développer une solution de recommandation de films qui repose sur des données réelles et utilise une approche de filtrage collaboratif. L'objectif est d'offrir une expérience utilisateur personnalisée en proposant une liste de films adaptés à leurs goûts et préférences, tout en permettant une analyse approfondie des données collectées.

---

Pour ce faire le projet sera séparé en trois parties :

- Un service base de données (DuckDB)

- Un service Backend (API)

- Un service Frontend (Dashboard)

--

Afin de lancer la collecte de donné:

-aller dans le fichier .env pour mettre votre clé api récolter sur tmdb, et sauvegarder le fichier.

-une fois fait aller dans backend/app/utils/data_from_api.py et lancer le script (ca va sauvegarder les données dans data/)

-une fois les données charger aller dans backend/app/utils/database_loading et lancer le script, ca va créer la base de donnéed data 

- un fichier jupt.ipynb est présent dans le dossier data pour s'approprier la base de donnée et faire quelques requete dessus, si besoin.(il y a une instruction pour supprimer les films dans la table  avec release_date vide, normalementc'est pas censé arrivé vue la construction de la table avec sqlalchemy, mais j'ai eu quelques problèmes avec ça dans la requete avec fastapi, donc si vous avez ce problème aller voir s'il y a des film avec release_date null)



L'Api pour la partie backend se trouve dans backend/main.py

Pour accéder à l'api et tester les endpoint faire  depuis le dossier Projets:
` uvicorn backend.main:app --port 8000 `

Ensuite une fois le serveur fastapi lancé rajouter /docs dans l'url  aprés   127.0.0.1:8000  pour tester les endpoints


Pour lancer les service en mode productions ,vous pouvez lancer  avec docker-compose les services grâce à

`docker-compose up`

Vous pouvez accéder à l'api ensuite une fois les conteneurs crée, et au dashboard

L'api est  accesssible au localhost:8000
Le dashboard est accessible au localhost:8501

