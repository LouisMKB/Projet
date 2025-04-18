import duckdb
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

DB_PATH = "data/movies.duckdb"

def plot_rating_distribution():
    con = duckdb.connect(DB_PATH)
    df = con.execute("SELECT vote_average FROM films").fetchdf()
    fig, ax = plt.subplots()
    sns.histplot(df["vote_average"], bins=20, kde=True, ax=ax)
    ax.set_title("Distribution des notes moyennes")
    st.pyplot(fig)

def plot_movies_by_year():
    con = duckdb.connect(DB_PATH)
    df = con.execute("""
        SELECT strftime('%Y', release_date) AS year, COUNT(*) AS count
        FROM films
        WHERE release_date IS NOT NULL
        GROUP BY year
        ORDER BY year
    """).fetchdf()
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x="year", y="count", ax=ax)
    ax.set_title("Nombre de films par année")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
