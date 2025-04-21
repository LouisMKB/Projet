
import streamlit as st
import requests

import streamlit as st
import requests
import os

# Récupère l'URL du backend depuis les variables d'environnement
backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

# Fonction pour appeler l'API du backend
def fetch_data():
    try:
        response = requests.get(f"{backend_url}/")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch data"}
    except Exception as e:
        return {"error": str(e)}
    
def fetch_data_2():
    try:
        response = requests.get(f"{backend_url}/films")
        if response.status_code == 200:
            films_data = response.json()
            films = films_data.get('films', [])  # Assure-toi que 'films' est une clé dans la réponse
            if not films:
                return {"error": "No films found in the response"}
            return films  # Retourne la liste des films
        else:
            return {"error": f"Failed to fetch films, Status Code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


# Utilise Streamlit pour afficher les données
st.title("Communication avec le Backend")
data = fetch_data()
if 'error' in data:
    st.error(f"Erreur: {data['error']}")
else:
    st.write("Message du backend:", data.get("message"))



# Utilise Streamlit pour afficher les données
st.title("Affiche les films")
data = fetch_data_2()

if 'error' in data:
    st.error(f"Erreur: {data['error']}")
else:
    # Si la réponse contient des films, afficher chaque film
    if isinstance(data, list) and data:  # Vérifier que data est une liste et non vide
        for film in data:
            st.write(f"**{film['title']}**")
            st.write(f"Genres: {film['genres']}")
            st.write(f"Description: {film['description']}")
            st.write(f"Release Date: {film['release_date']}")
            st.write(f"Vote Average: {film['vote_average']}")
            st.write("---")
    else:
        st.write("Aucun film trouvé.")


# def fetch_poster(movie_id):
#     url="https://api/themoviedb.org/3/movie/{}?api_key=".format(movie_id)
#     data=requests.get(url)
#     data=data.json()
#     poster_path=data['poster_path']
#     full_path="https://image.tmdb/org/t/p/w500/" + poster_path
#     return full_path
# movies=[]
# similarity=[]
# movies_list=["peter pan ","asterix"]

# st.header("Movie recommandation system")
# #create a dropdown to select a movie
# selected_movies=st.selectbox("Select a movie",movies_list)

# def recommend(movie):
#     index=movies[movies['title']==movie].index[0]
#     distance = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda vector: vector[1])
#     recommend_movie=[]
#     recommend_poster=[]
#     for i in distance[1:6]:
#         movie_id=movies.iloc[i[0]].id
#         recommend_movie.append(movies.iloc[i[0].title])
#         recommend_poster.append(fetch_poster(movies_id))
#     return recommend_movie,recommend_poster

# if st.button("Show Recommend"):
#     movie_name, movie_poster =recommend(selected_movies)
#     col1,col2,col3,col4,col5 = st.columns(5)
#     with col1:
#         st.text(movie_name[0])
#         st.image(movie_poster[0])
#     with col2:
#         st.text(movie_name[1])
#         st.image(movie_poster[1])
#     with col3:
#         st.text(movie_name[2])
#         st.image(movie_poster[2])
#     with col4:
#         st.text(movie_name[3])
#         st.image(movie_poster[3])   
#     with col5:
#         st.text(movie_name[4])
#         st.image(movie_poster[4])   




# pressed= st.button("press me")
# print("1",pressed)
# pressed2= st.button("press me 2")
# print("2",pressed2)

# if "step" not in st.session_state:
#     st.session_state.step =1

# st.sidebar.title('title of the sidebar')
# st.sidebar.write("you can place elements here")
# st.sidebar.text_input("enter sth")
