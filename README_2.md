# Projet sur la recommendation de films

## NOM Prénom :

- KOUMBA BOUNDA Louis-Marie
- LECLERC Cédric
- DORIVAL Pierre-Chrislin

### **Pour rappel voici le contexte du projet :** 
En tant que plateforme de streaming de contenus audiovisuels, nous souhaitons développer une solution de recommandation de films qui repose sur des données réelles et utilise une approche de filtrage collaboratif. L'objectif est d'offrir une expérience utilisateur personnalisée en proposant une liste de films adaptés à leurs goûts et préférences, tout en permettant une analyse approfondie des données collectées.

---

Pour ce faire le projet sera séparé en trois parties :

- Un service base de données (DuckDB)

- Un service Backend (API)

- Un service Frontend (Dashboard)

--
\\
_______

### Récuperer le projet
Créer un dossier et ouvrez le  avec vscode, ouvrez un terminal et faite
`git clone https://github.com/LouisMKB/Projet.git` dans votre terminal

Dans ce projet, vue que nous utilisons un fichier .db en local et que nous avons stocké les données sur github, vous n'avez pas besoin de lancer l'environnement de développement, pour récupérer les données et créer la base de donnée  avant de pouvoir lancer l'application.


__________

### Lancer en mode production le projet
Pour lancer les services en mode production et profiter de l'application de recommendation de film  Homeflix,vous pouvez lancer docker desktop sur votre machine  et ensuite taper dans votre terminal

`docker compose up --build`

Cela lance la construction de 2 images, une pour le frontend et une pour le backend, cela peut prendre quelques minutes.

Vous pouvez accéder à l'api ensuite une fois les conteneurs crée, et au dashboard
- L'API est accessible à l'adresse suivante : [http://localhost:8000](http://localhost:8000)
- Le dashboard est accessible ici : [http://localhost:8501](http://localhost:8501)


### Lancer en mode développement le projet
#### Configuration de l'environnement de développement.

Voici 2 approches:
#####  Approche 1
1. Initialisation de l'environnement virtuelle
Afin d'initialiser l'environnement de développement, à la racine du projet écrire
Sur linux:
-  `python3 -m venv .venv` 
- `Source .venv/bin/activate`

Sur windows:

- `python -m venv .venv` 
- `.venv/Scripts/activate`

2. Installation des dépendances:
`pip install -r requirements.txt`

##### Approche alternative (plus rapide)

- `pip install uv` ou `pip3 install uv`
- `uv init` (uv initialise un environnement virtuelle à notre place)
- `uv add -r requirments.txt` (uv est plus rapide que pip pour installer les dépendances)


#### Collecte des données depuis l'api, et insertion dans une base de donnée.


Afin de lancer la collecte de donnée:

- Créer un fichier  `.env` à la racine du projet pour mettre votre clé api , ou ici  le TMDB_BEARER_TOKEN récolter sur TMDB, et sauvegarder le fichier.

Vous devez  ecrire dans le fichier `.env` le code suivant avec un code valide que vous pouvez vous procurez en vous inscrivant à TMDB et en demandant une clé api.

```TMDB_BEARER_TOKEN=eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhMzM0NmU2ZWI2NGY0MGYxNmM2NzNiZTZmYjBlMzFkYyIsIm5iZiI6MTc0NDQ2NDIxNS4wNTMsInN1YiI6IjY3ZmE2OTU3ZDRjNDQ0YTFjYzlhMGY3MSIsInNjbI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.N0wT0FCQMKVFdHF6A3vP9HCdSefoKeg7pZLzfQTSVKA```

Ce TMDB_BEARER_TOKEN n'est pas valide,procurez vous en un valide sur le site TMDB.

Une fois que vous avez fait cela,aller dans `backend/app/utils/data_from_api.py` et lancer le script depuis l'éxecutable python  en haut à droite dans vscode (ca va sauvegarder les données dans backend/app/utils/data/)

Une fois les données charger aller dans `backend/app/utils/database_loading` et lancer le script de la même manière, ca va créer la base de donnée `film_reco.db` et la remplir. 

- un fichier jupt.ipynb est présent dans le dossier data pour s'approprier la base de donnée et faire quelques requête dessus, si besoin.(il y a une instruction pour supprimer les films dans la table  avec release_date vide, normalementc'est pas censé arrivé vue la construction de la table avec sqlalchemy, mais j'ai eu quelques problèmes avec ça dans la requete avec fastapi, donc si vous avez ce problème aller voir s'il y à des films avec release_date null)


______________

##### Lancer l'api en mode dév pour débugger

L'Api pour la partie backend se trouve dans backend/main.py

Pour accéder à l'api et tester les endpoint faire  depuis la racine du projet
` uvicorn backend.main:app --port 8000 --reload` --reload est pour relancer  automatiquement le serveur uvicorn en cas de changement dans le code 

Ensuite une fois le serveur fastapi lancé, aller sur  [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) pour tester les endpoints.


