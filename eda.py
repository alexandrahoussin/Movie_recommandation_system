import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
from datetime import datetime, date
from PIL import Image

def app():
    
    st.markdown("<h1 style = 'text-align : center; color: #F73C29;'> Exploration des données et KPI </h1>", unsafe_allow_html=True)
    st.write("Dans cette partie vous pourrez voir notre exploration de données des datasets IMDB.")
    st.write("Le dataset comporte plusieurs types de titres (courts-métrages, séries, films)... Nous n'avons concentré nos KPI seulement sur les films.")
    option = st.selectbox('Que souhaitez-vous voir?', ('La production de films à travers les décénnies',
                                                       'Top films', 'Les genres', 'les acteurs et actrices', 'Les points communs des films du top 100'))
    @st.cache
    def get_movies_rating():
        return pd.read_csv('data/final_movie_rating.csv.zip', index_col=0)
    
    @st.cache
    def get_top100():
        return pd.read_csv('data/top_100.csv.zip', index_col=0)
    
    @st.cache
    def get_top_10_actors():
        return pd.read_csv('data/top_10_actors.csv.zip', index_col=0)
    
    @st.cache
    def get_actors():
        return pd.read_csv('data/actors_df.csv.zip', index_col=0)
    
    @st.cache
    def get_top_real():
        return pd.read_csv('data/top_real.csv.zip', index_col=0)
    final_movie_rating = get_movies_rating()
    top_100 = get_top100()
    top_10_actors = get_top_10_actors()
    actors_df = get_actors()
    top_real = get_top_real()
    

    if option == 'La production de films à travers les décénnies':
        st.subheader('La production de films à travers les décénnies')
        col1, col2 = st.columns(2)
        col1.write("La grande majorité des films ont été produits entre les années 2000 et aujourd'hui. Nous pouvons noter une réelle augmentation de ce nombre entre 2010 et 2020. Ce chiffre peut s'expliquer potentiellement par l'arrivée sur le marché des différentes plateformes de streaming (Netflix, Amazon prime Vidéos etc).")
        fig = px.histogram(final_movie_rating, x='decade',
                        title = 'Nombre de films sortis par décénnie', color_discrete_sequence=['rgb(237,100,90)'],
                        category_orders = {'decade' : ['<1900', '1900 - 1910', "1910 - 1920", "1920 - 1930", "1930 - 1940","1940 - 1950",
                                                        "1950 - 1960", "1960 - 1970","1970 - 1980", "1980 - 1990", "1990 - 2000", "2000 - 2010", 
                                                        "2010 - 2020", "2020 - 2030" ]}, template= 'plotly')
        fig.update_layout(title= {'x' : 0.5}, hoverlabel=dict(bgcolor="white"))
        fig.update_xaxes(title_text = '')
        fig.update_yaxes(title_text = '')
        col1.plotly_chart(fig, use_container_width=True)
        
        col2.write("Comme vu précédemment le nombre de sorties de films n'a cessé d'augmenter depuis les années 20. Avec la Covid 19, on constate une baisse drastique des sorties depuis 2019, les cinémas du monde entier ayant été fermés.")
        movies_rating_dropna_year = final_movie_rating[(final_movie_rating['runtimeMinutes'] >= 60) & (final_movie_rating['runtimeMinutes'] <240)]
        fig = px.area(x=movies_rating_dropna_year['startYear'].value_counts().index, 
                    y=movies_rating_dropna_year['startYear'].value_counts().values,
                    title = "Nombre de films sortis par année", color_discrete_sequence=['rgb(237,100,90)'], template= 'simple_white')
        annot = { 'x' : 2020, 'y' : 6202, 'showarrow' : True, 'arrowsize' : 2, 'arrowwidth' :1,
                'arrowhead': 5, 'text' : "Baisse du nombre de sorties en 2020",
                'font' : {'size' : 12}}
        fig.update_traces(hovertemplate=None)
        fig.update_layout({'annotations' : [annot]}, title= {'x' : 0.5}, hovermode = 'x', hoverlabel=dict(
            bgcolor="white"))
        fig.update_xaxes(title_text = '')
        fig.update_yaxes(title_text = '')
        col2.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        after_1920 = movies_rating_dropna_year[movies_rating_dropna_year['startYear'] > 1920]
        pivot1 = after_1920.pivot_table(index='startYear', values='runtimeMinutes', aggfunc='mean')
        fig= px.line(pivot1, x=pivot1.index, y='runtimeMinutes', 
                    title = "Durée moyenne des films par année ", color_discrete_sequence=['rgb(237,100,90)'], template= 'simple_white')
        fig.update_traces(hovertemplate=None)
        fig.update_layout(title= {'x' : 0.5}, xaxis = dict(dtick = 10),hovermode = 'x', hoverlabel=dict(
            bgcolor="white"))
        fig.update_xaxes(title_text = '')
        fig.update_yaxes(title_text = '')
        col2.plotly_chart(fig, use_container_width=True)
        col2.write("Entre 1920 et 1992, la durée moyenne des films n'a fait qu'augmenter pour atteindre une durée de 100 minutes. Celle-ci a ensuite connu une baisse jusqu'en 2012 pour remonter à nouveau. ")
    
    if option == 'Top films': 
        st.subheader('Top des films')
        st.write('Nous avons décidé de faire une étude sur le top 100 des films. Ceux-ci ont été classés par nombre de votes puis par la moyenne des notes.')
        st.write('Quels sont les 10 films les plus et les mieux notés ?')
                
        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
        shaw = Image.open('assets/shawshank.jpg')
        col1.image(shaw, width = 150)
        col1.markdown("<p style = 'text-align : center;'> 2.488.195 votes </p>", unsafe_allow_html=True)
        col1.markdown("<p style = 'text-align : center;'> Note moyenne: 9.3 </p>", unsafe_allow_html=True)
        dark = Image.open('assets/darkknight.jpg')
        col2.image(dark, width = 172)
        col2.markdown("<p style = 'text-align : center;'> 2.441.388 votes </p>", unsafe_allow_html=True)
        col2.markdown("<p style = 'text-align : center;'> Note moyenne: 9 </p>", unsafe_allow_html=True)
        incept = Image.open('assets/inception.jpg')
        col3.image(incept)
        col3.markdown("<p style = 'text-align : center;'> 2.190.799 votes </p>", unsafe_allow_html=True)
        col3.markdown("<p style = 'text-align : center;'> Note moyenne: 8.8 </p>", unsafe_allow_html=True)
        fight = Image.open('assets/fightclub.jpg')
        col4.image(fight, width = 172)
        col4.markdown("<p style = 'text-align : center;'> 1.959.929 votes </p>", unsafe_allow_html=True)
        col4.markdown("<p style = 'text-align : center;'> Note moyenne: 8.8 </p>", unsafe_allow_html=True)
        pulp = Image.open('assets/pulp.jpg')
        col5.image(pulp, width = 172)
        col5.markdown("<p style = 'text-align : center;'> 1.924.045 votes </p>", unsafe_allow_html=True)
        col5.markdown("<p style = 'text-align : center;'> Note moyenne: 8.9 </p>", unsafe_allow_html=True)
        forest = Image.open('assets/forest.jpg')
        col6.image(forest, width = 163)
        col6.markdown("<p style = 'text-align : center;'> 1.922.897 votes </p>", unsafe_allow_html=True)
        col6.markdown("<p style = 'text-align : center;'> Note moyenne: 8.8 </p>", unsafe_allow_html=True)
        matrix = Image.open('assets/matrix.jpg')
        col7.image(matrix, width = 172)
        col7.markdown("<p style = 'text-align : center;'> 1.776.732 votes </p>", unsafe_allow_html=True)
        col7.markdown("<p style = 'text-align : center;'> Note moyenne: 8.7 </p>", unsafe_allow_html=True)
        lord1 = Image.open('assets/lord.jpg')
        col8.image(lord1, width = 157)
        col8.markdown("<p style = 'text-align : center;'> 1.743.718 votes </p>", unsafe_allow_html=True)
        col8.markdown("<p style = 'text-align : center;'> Note moyenne: 8.8 </p>", unsafe_allow_html=True)
        lord2 = Image.open('assets/lordreturn.jpg')
        col9.image(lord2, width = 155)
        col9.markdown("<p style = 'text-align : center;'> 1.722.424 votes </p>", unsafe_allow_html=True)
        col9.markdown("<p style = 'text-align : center;'> Note moyenne: 8.9 </p>", unsafe_allow_html=True)
        god = Image.open('assets/godfather.jpg')
        col10.image(god, width = 155)
        col10.markdown("<p style = 'text-align : center;'> 1.717.256 votes </p>", unsafe_allow_html=True)
        col10.markdown("<p style = 'text-align : center;'> Note moyenne: 9.2 </p>", unsafe_allow_html=True)
        
        
        
    if option == 'Les genres':
        st.subheader('Les genres')
        
        st.write('Le genre principal le plus représenté parmis les films est Drame, suivi par les comédies et les documentaires.')
        fig = px.histogram(final_movie_rating, x='genre 1',
                        title = 'Nombre de films par genre principal', color_discrete_sequence=['rgb(237,100,90)'], template= 'plotly')
        fig.update_layout(title= {'x' : 0.5}, hoverlabel=dict(bgcolor="white"))
        fig.update_xaxes(title_text = '')
        fig.update_yaxes(title_text = '')
        st.plotly_chart(fig, use_container_width=True)
        
    
    if option == 'les acteurs et actrices':
        st.subheader('Les acteurs / actrices')
        col1, col2 = st.columns(2)
        col2.write("Dans cette partie de l'exploration nous avons divisé les données pour ne garder que les acteurs et actrices par film.")        
        col2.write('Nous avons souhaité étudier la répartition des acteurs et actrices par âge et par nombre de films. Pour cela nous avons utilisé le top 100 des films.')
        col2.write('Dans ce top 100, nous pouvons remarquer que les hommes sont plus représentés. Les femmes, font moins de films passé 50 ans.')
        fig = px.histogram(actors_df, x='age_fork', color = 'category',
                        title = 'Nombre de films par age des acteurs et actrices', 
                        color_discrete_sequence=[ 'rgb(237,100,90)','rgb(251,180,174)'], template= 'plotly',
                        category_orders = {'age_fork': ['<18', '18-30', '30-40', '40-50', '50-60', '60-70', '> 70']})
        fig.update_layout(title= {'x' : 0.5}, hoverlabel=dict(bgcolor="white"), legend_title_text= (''))
        fig.update_xaxes(title_text = '')
        fig.update_yaxes(title_text = '')
        col1.plotly_chart(fig, use_container_width=True)
    
    if option == 'Les points communs des films du top 100':
        st.subheader("Les films du top 100 ont-ils des points communs ?  ")
        st.write("Les films du top 100 sont majoritairement des films d'action. Les notes des films de ce top, varient en moyenne entre 8 et 8.5. Les mieux notés sont les films de crime.")
        movie_col, serie_col = st.columns(2)
        
        movies_vote_genre = top_100.pivot_table(index='genre 1', values='numVotes',aggfunc='sum')
        movies_vote_genre.sort_values(by='numVotes', ascending = False)
        movies10_vote_genre = movies_vote_genre.sort_values(by='numVotes', ascending = False)[:10]
        fig = px.bar(x=movies10_vote_genre.index,
                    y =movies10_vote_genre['numVotes'],
                        title = 'Nombre de votes par genre', color_discrete_sequence=['rgb(249,166,166)'], template= 'plotly')
        fig.update_layout(title= {'x' : 0.5}, hoverlabel=dict(bgcolor="white"))
        fig.update_xaxes(title_text = '')
        fig.update_yaxes(title_text = '')
        movie_col.plotly_chart(fig, use_container_width=True)
        
        movies_rating_genre = top_100.pivot_table(index='genre 1', values='averageRating')
        movies_rating_genre = movies_rating_genre.sort_values(by='averageRating', ascending = False)[:10] 
        fig = px.bar(x=movies_rating_genre.index,
                    y =movies_rating_genre['averageRating'],
                        title = 'Moyenne des notes des films par genre', color_discrete_sequence=['rgb(237,100,90)'], template= 'plotly')
        fig.update_layout(title= {'x' : 0.5}, hoverlabel=dict(bgcolor="white"))
        fig.update_xaxes(title_text = '')
        fig.update_yaxes(title_text = '')
        serie_col.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        
        
        
        top_real_df = top_real['primaryName'].value_counts()[:10]
        st.write('Quels sont les réalisateurs les plus présents dans ce top 100 ?')
        fig = px.bar(x=top_real_df.index,
                    y = top_real_df.values,
                        title = 'Les 10 réalisateurs les plus présents dans le top 100 des films', color_discrete_sequence=['rgb(249,166,166)'], template= 'plotly')
        fig.update_layout(title= {'x' : 0.5}, hoverlabel=dict(bgcolor="white"))
        fig.update_xaxes(title_text = '')
        fig.update_yaxes(title_text = '')
        st.plotly_chart(fig, use_container_width=True)
        st.write('Christopher Nolan a réalisé 7 films du top 100 et arrive premier de ce classement. Nous retrouvons également avec 5 films dans le classement : Martin Scorsese, Steven Spielberg et Tanrantino.')
        
        top_decade = top_100['decade'].value_counts()
        fig = px.bar(x=top_decade.index,
                    y = top_decade.values,
                        title = 'Nombre de top films sortis par décénnie',  color_discrete_sequence=['rgb(247,120,120)'], template= 'plotly')
        fig.update_layout(title= {'x' : 0.5}, hoverlabel=dict(bgcolor="white"))
        fig.update_xaxes(title_text = '')
        fig.update_yaxes(title_text = '')
        st.plotly_chart(fig, use_container_width=True)
        st.write('Plus de la moitié des films du top 100 sont sortis après 2000.')
        st.write("Nous n'avons pas préconisé au client de se spécialiser dans un genre de film précis. ")
        st.write("Par contre, nous lui proposons de faire des évènements thèmatiques.")
        st.write("Par exemple il pourrait faire :")
        st.write("- une semaine Christopher Nolan,")
        st.write("- un weekend Dicaprio,")
        st.write("- un festival de film d'action,")
        
        
        
    