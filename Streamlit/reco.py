import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors


def app():
    
    st.markdown("<h1 style = 'text-align : center'> Recommandation de films </h1>", unsafe_allow_html=True)
    st.write("Dis-nous ce que tu aimes, on te dira quoi regarder !")
    
    @st.cache
    def get_df():
        movies_df = pd.read_csv('df_algo.csv')
        return movies_df
    
    movies_df = get_df()
    
    @st.cache
    def get_list_from_partial_title(title):
        title = title.lower()
        movies_lower = movies_lower = movies_df.copy()
        movies_lower['primaryTitle'] = movies_lower['primaryTitle'].str.lower()
        list_movies= movies_lower[movies_lower['primaryTitle'].str.contains(title)].index.tolist()
        df = movies_df.iloc[list_movies, :]
        titres = []
        for key, value in df.iteritems() :
            if key == 'primaryTitle':
                titres.append(value)
        return df['primaryTitle']
    
    
    
    # Algo
    colonnes = list(movies_df.columns)
    col = colonnes[9:]
    X = movies_df[col]
    # entrainement du modèle
    model2 = NearestNeighbors(n_neighbors=6, metric='cosine').fit(X)
    # assigner les distances et les indices obtenus 
    distances, indices = model2.kneighbors(X)
    
    
    # display les titres proches 
    @st.cache   
    def get_movies(title):
        def get_index(title):
            return movies_df[movies_df['primaryTitle'] == title].index.tolist()[0]
        movie_id = get_index(title)
        return movies_df.iloc[indices[movie_id], 3]
    
    user_title = st.text_input('Titre de ton film préféré:')
    liste_titre = get_list_from_partial_title(user_title)
    if user_title:
        choice = st.selectbox('Choisis le bon film:', liste_titre )
        col1, col2, col3 = st.columns(3)
        if col2.button("C'est parti !"):
            col2.write(f"Voici une liste de films qui devrait te plaire si tu as aimé {choice}:")
            result = list(get_movies(choice))[1:]
            for f in result :
                col2.write(f'- {f}')
    
    
    
    