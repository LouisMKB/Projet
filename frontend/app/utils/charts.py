# utils/charts.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="whitegrid")

def plot_rating_distribution(movies):
    df = pd.DataFrame(movies)
    fig, ax = plt.subplots()
    sns.histplot(df["vote_average"], bins=20, kde=True, ax=ax)
    ax.set_title("Distribution des notes")
    st.pyplot(fig)

def plot_movies_per_year(movies):
    df = pd.DataFrame(movies)
    df["release_date"] = pd.to_datetime(df["release_date"], errors='coerce')
    df["year"] = df["release_date"].dt.year
    count_by_year = df["year"].value_counts().sort_index()
    fig, ax = plt.subplots()
    count_by_year.plot(kind="bar", ax=ax)
    ax.set_title("Nombre de films par an")
    st.pyplot(fig)

def plot_top_movies(movies, top_n=10):
    df = pd.DataFrame(movies)
    top_movies = df.sort_values("vote_average", ascending=False).head(top_n)
    fig, ax = plt.subplots()
    sns.barplot(data=top_movies, x="vote_average", y="title", ax=ax)
    ax.set_title(f"Top {top_n} films par note")
    st.pyplot(fig)
