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
