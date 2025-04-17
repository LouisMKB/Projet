import streamlit as st
import requests

def fetch_poster(movie_id):
    url="https://api/themoviedb.org/3/movie/{}?api_key=".format(movie_id)
    data=requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    full_path="https://image.tmdb/org/t/p/w500/" + poster_path
    return full_path
movies=[]
similarity=[]
movies_list=["peter pan ","asterix"]

st.header("Movie recommandation system")
#create a dropdown to select a movie
selected_movies=st.selectbox("Select a movie",movies_list)

def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda vector: vector[1])
    recommend_movie=[]
    recommend_poster=[]
    for i in distance[1:6]:
        movie_id=movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0].title])
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie,recommend_poster

if st.button("Show Recommend"):
    movie_name, movie_poster =recommend(selected_movies)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])   
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])   




pressed= st.button("press me")
print("1",pressed)
pressed2= st.button("press me 2")
print("2",pressed2)

if "step" not in st.session_state:
    st.session_state.step =1

st.sidebar.title('title of the sidebar')
st.sidebar.write("you can place elements here")
st.sidebar.text_input("enter sth")