import pandas as pd

def cargar_datos(path):
    df = pd.read_csv(path)

    # Limpiar columna Votes (elimina comas y convierte a número)
    df['Votes'] = df['Votes'].astype(str).str.replace(',', '', regex=False)
    df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce')

    # Limpiar columna Gross (elimina $ y M, convierte a número)
    df['Gross'] = df['Gross'].astype(str).str.replace(r'[\$,M]', '', regex=True)
    df['Gross'] = pd.to_numeric(df['Gross'], errors='coerce')

    # Asegurar que Rating sea numérico
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

    # Eliminar filas sin título o rating
    df = df.dropna(subset=['Movie Title', 'Rating'])

    return df

def recomendar_peliculas(df, top_n=10, min_votos=10000, min_rating=None, min_year=None):
    # Filtrar por votos
    df_filtrado = df[df['Votes'] >= min_votos]

    # Filtrar por rating si se especifica
    if min_rating is not None:
        df_filtrado = df_filtrado[df_filtrado['Rating'] >= min_rating]

    # Filtrar por año si se especifica
    if min_year is not None:
        df_filtrado = df_filtrado[df_filtrado['Movie Year'] >= min_year]

    # Seleccionar películas random
    recomendaciones = df_filtrado.sample(n=min(top_n, len(df_filtrado)), random_state=42)

    return recomendaciones[['Movie Title', 'Movie Year', 'Rating']]

if __name__ == '__main__':
    df_peliculas = cargar_datos('data/horror_movies.csv')

    try:
        min_year = int(input("Ingresá el año mínimo de las películas: "))
    except ValueError:
        min_year = None

    try:
        min_rating = float(input("Ingresá el rating mínimo: "))
    except ValueError:
        min_rating = None

    try:
        top_n = int(input("¿Cuántas recomendaciones querés ver?: "))
    except ValueError:
        top_n = 5

    recomendadas = recomendar_peliculas(df_peliculas, top_n=top_n, min_rating=min_rating, min_year=min_year)

    print("\n🎬 Recomendaciones de películas de terror:\n")
    print(recomendadas.to_string(index=False))