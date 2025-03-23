import streamlit as st
import pandas as pd
from main import cargar_datos, recomendar_peliculas

# Cargar datos
df = cargar_datos('data/horror_movies.csv')

st.title("FearFinder")
st.subheader("Recomendador de películas de terror")

# Filtros
min_year = st.slider("Año mínimo", 1960, 2025, 2000)
min_rating = st.slider("Rating mínimo", 0.0, 10.0, 6.5)
top_n = st.slider("Cantidad de películas a recomendar", 1, 20, 5)

# Botón
if st.button("Buscar recomendaciones"):
    recomendaciones = recomendar_peliculas(
        df, top_n=top_n, min_rating=min_rating, min_year=min_year
    )
    st.write("📽️ Películas recomendadas:")
    for _, row in recomendaciones.iterrows():
        st.markdown(f"### 🎬 {row['Movie Title']} ({int(row['Movie Year'])})")
        st.markdown(f"**Rating:** ⭐ {row['Rating']}")
        if 'Description' in row and pd.notna(row['Description']):
            st.markdown(f"**Sinopsis:** {row['Description']}")
        st.markdown("---")