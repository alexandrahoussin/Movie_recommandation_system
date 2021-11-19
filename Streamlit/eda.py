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
    def df_movies():
        title_basics1 = pd.read_csv('https://datasets.imdbws.com/title.basics.tsv.gz', sep ='\t', low_memory = False)
        title_basics1 = title_basics1.replace('\\N', np.NaN)
        title_basics1 = title_basics1[title_basics1['isAdult'] == '0']
        title_basics1['runtimeMinutes'] = title_basics1['runtimeMinutes'].replace('Reality-TV', np.NaN)
        title_basics1['runtimeMinutes'] = title_basics1['runtimeMinutes'].replace('Documentary', np.NaN)
        title_basics1['runtimeMinutes'] = title_basics1['runtimeMinutes'].replace('Talk-Show', np.NaN)
        title_basics1['runtimeMinutes'] = title_basics1['runtimeMinutes'].replace('Game-Show', np.NaN)
        title_basics1['runtimeMinutes'] = title_basics1['runtimeMinutes'].replace('Animation,Comedy,Family', np.NaN)
        title_basics1['runtimeMinutes'] = title_basics1['runtimeMinutes'].astype(float)
        
        movies_genre = title_basics1.copy()
        df_genre2 = title_basics1['genres'].str.split(',', expand=True)
        movies_genre['genre 1'] = df_genre2[0]
        movies_genre['genre 2'] = df_genre2[1]
        movies_genre['genre 3'] = df_genre2[2]
        movies_genre = movies_genre[movies_genre['titleType'] =='movie']
        return movies_genre
    
    movies = df_movies()
    
    
    @st.cache
    def movie_rating():
        title_ratings= pd.read_csv('https://datasets.imdbws.com/title.ratings.tsv.gz', sep = '\t')
        movie_rating = movies.merge(title_ratings, on='tconst', how='inner')
        return movie_rating 
    
    movie_rating = movie_rating()
    
    movies_rating_dropna_year = movie_rating[movie_rating['startYear'].notna()].copy()
    movies_rating_dropna_year['startYear'] = movies_rating_dropna_year['startYear'].astype(int)
    
    def decennie(x):
        if x < 1900:
            return '<1900'
        elif 1900 <= x < 1910:
            return '1900 - 1910'
        elif 1910 <= x < 1920:
            return "1910 - 1920"
        elif 1920 <= x < 1930:
            return "1920 - 1930"
        elif 1930 <= x < 1940:
            return "1930 - 1940"
        elif 1940 <= x < 1950:
            return "1940 - 1950"
        elif 1950 <= x < 1960:
            return "1950 - 1960"
        elif 1960 <= x < 1970:
            return "1960 - 1970"
        elif 1970 <= x < 1980:
            return "1970 - 1980"
        elif 1980<= x < 1990:
            return "1980 - 1990"
        elif 1990 <= x < 2000:
            return "1990 - 2000"
        elif 2000 <= x < 2010:
            return "2000 - 2010"
        elif 2010 <= x < 2020:
            return "2010 - 2020"
        elif 2020 <= x < 2030:
            return "2020 - 2030"

    movies_rating_dropna_year['decade'] = movies_rating_dropna_year['startYear'].apply(decennie)
    pivot_top100 = movie_rating.pivot_table(index=['primaryTitle', 'tconst'], values = ['averageRating', 'numVotes'])
    top100 = pivot_top100.sort_values(['numVotes'], ascending=[False])[:100]
    top100_df = pd.DataFrame(top100)
    
    @st.cache
    def get_actors():
        principals = pd.read_csv('https://datasets.imdbws.com/title.principals.tsv.gz', sep ='\t', usecols=['tconst', 'nconst', 'category'])
        actors_df = principals[(principals['category'] == 'actor')|(principals['category'] == 'actress')]
        names = pd.read_csv("https://datasets.imdbws.com/name.basics.tsv.gz", sep ='\t')
        actors = actors_df.merge(names, how = 'inner', on = 'nconst')
        actors.drop(['primaryProfession', 'knownForTitles'], axis = 1, inplace = True)
        actors = actors.replace('\\N', np.NaN)
        actors['category'] = actors['category'].astype('category')
        actors_clean = actors.copy().dropna(subset=['birthYear'])
        actors_sans_death = actors_clean[actors_clean['deathYear'].isna()]
        living_actors = actors_sans_death.copy()
        living_actors.drop(columns=['deathYear'], inplace=True)
        living_actors['birthYear'] = living_actors['birthYear'].astype(int)
        living_actors.drop(living_actors[living_actors['birthYear'] == 21].index, inplace=True)
        def age(birthY):
            today = date.today()
            return today.year - birthY
        living_actors['age'] = living_actors['birthYear'].apply(age)
        living_actors.drop(living_actors[living_actors['age'] > 120].index, inplace=True)
        def age_period(age):
            if age < 18:
                return '<18'
            elif 18 <=age < 30:
                return '18-30'
            elif 30 <=age < 40:
                return '30-40'
            elif 40 <=age < 50:
                return '40-50'
            elif 50 <= age < 60:
                return '50-60'
            elif 60 <=age < 70:
                return '60-70'
            elif age >= 70:
                return '> 70'
        living_actors['age_fork'] = living_actors['age'].apply(age_period)
        top = top100_df.merge(living_actors, how = 'inner', on = 'tconst')
        return top
    
    actors = get_actors()
    top100_df_bis = movies_rating_dropna_year.sort_values(['numVotes', 'averageRating'], ascending = False)[:100]
    top_100_actors = top100_df_bis.merge(actors, how='inner', on = 'tconst')
    
    @st.cache
    def get_real():
        principals = pd.read_csv('https://datasets.imdbws.com/title.principals.tsv.gz', sep ='\t', usecols=['tconst', 'nconst', 'category'])
        real_df = principals[principals['category'] == 'director']
        top_real = top100_df_bis.merge(real_df, how='left', on = 'tconst')
        names = pd.read_csv("https://datasets.imdbws.com/name.basics.tsv.gz", sep ='\t')
        top_real_df = top_real.merge(names, how = 'left', on = 'nconst')
        return top_real_df
    
    top_real_df = get_real()
    
    if option == 'La production de films à travers les décénnies':
        st.subheader('La production de films à travers les décénnies')
        col1, col2 = st.columns(2)
        col1.write("La grande majorité des films ont été produits entre les années 2000 et aujourd'hui. Nous pouvons noter une réelle augmentation de ce nombre entre 2010 et 2020. Ce chiffre peut s'expliquer potentiellement par l'arrivée sur le marché des différentes plateformes de streaming (Netflix, Amazon prime Vidéos etc).")
        fig = px.histogram(movies_rating_dropna_year, x='decade',
                        title = 'Nombre de films sortis par décénnie', color_discrete_sequence=['rgb(237,100,90)'],
                        category_orders = {'decade' : ['<1900', '1900 - 1910', "1910 - 1920", "1920 - 1930", "1930 - 1940","1940 - 1950",
                                                        "1950 - 1960", "1960 - 1970","1970 - 1980", "1980 - 1990", "1990 - 2000", "2000 - 2010", 
                                                        "2010 - 2020", "2020 - 2030" ]}, template= 'plotly')
        fig.update_layout(title= {'x' : 0.5}, hoverlabel=dict(bgcolor="white"))
        fig.update_xaxes(title_text = '')
        fig.update_yaxes(title_text = '')
        col1.plotly_chart(fig, use_container_width=True)
        
        col2.write("Comme vu précédemment le nombre de sorties de films n'a cessé d'augmenter depuis les années 20. Avec la Covid 19, on constate une baisse drastique des sorties depuis 2019, les cinémas du monde entier ayant été fermés.")
        movies_rating_dropna_year = movies_rating_dropna_year[(movies_rating_dropna_year['runtimeMinutes'] >= 60) & (movies_rating_dropna_year['runtimeMinutes'] <240)]
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
        shaw = Image.open('shawshank.jpg')
        col1.image(shaw, width = 150)
        col1.markdown("<p style = 'text-align : center;'> 2.488.195 votes </p>", unsafe_allow_html=True)
        col1.markdown("<p style = 'text-align : center;'> Note moyenne: 9.3 </p>", unsafe_allow_html=True)
        dark = Image.open('darkknight.jpg')
        col2.image(dark, width = 172)
        col2.markdown("<p style = 'text-align : center;'> 2.441.388 votes </p>", unsafe_allow_html=True)
        col2.markdown("<p style = 'text-align : center;'> Note moyenne: 9 </p>", unsafe_allow_html=True)
        incept = Image.open('inception.jpg')
        col3.image(incept)
        col3.markdown("<p style = 'text-align : center;'> 2.190.799 votes </p>", unsafe_allow_html=True)
        col3.markdown("<p style = 'text-align : center;'> Note moyenne: 8.8 </p>", unsafe_allow_html=True)
        fight = Image.open('fightclub.jpg')
        col4.image(fight, width = 172)
        col4.markdown("<p style = 'text-align : center;'> 1.959.929 votes </p>", unsafe_allow_html=True)
        col4.markdown("<p style = 'text-align : center;'> Note moyenne: 8.8 </p>", unsafe_allow_html=True)
        pulp = Image.open('pulp.jpg')
        col5.image(pulp, width = 172)
        col5.markdown("<p style = 'text-align : center;'> 1.924.045 votes </p>", unsafe_allow_html=True)
        col5.markdown("<p style = 'text-align : center;'> Note moyenne: 8.9 </p>", unsafe_allow_html=True)
        forest = Image.open('forest.jpg')
        col6.image(forest, width = 163)
        col6.markdown("<p style = 'text-align : center;'> 1.922.897 votes </p>", unsafe_allow_html=True)
        col6.markdown("<p style = 'text-align : center;'> Note moyenne: 8.8 </p>", unsafe_allow_html=True)
        matrix = Image.open('matrix.jpg')
        col7.image(matrix, width = 172)
        col7.markdown("<p style = 'text-align : center;'> 1.776.732 votes </p>", unsafe_allow_html=True)
        col7.markdown("<p style = 'text-align : center;'> Note moyenne: 8.7 </p>", unsafe_allow_html=True)
        lord1 = Image.open('lord.jpg')
        col8.image(lord1, width = 157)
        col8.markdown("<p style = 'text-align : center;'> 1.743.718 votes </p>", unsafe_allow_html=True)
        col8.markdown("<p style = 'text-align : center;'> Note moyenne: 8.8 </p>", unsafe_allow_html=True)
        lord2 = Image.open('lordreturn.jpg')
        col9.image(lord2, width = 155)
        col9.markdown("<p style = 'text-align : center;'> 1.722.424 votes </p>", unsafe_allow_html=True)
        col9.markdown("<p style = 'text-align : center;'> Note moyenne: 8.9 </p>", unsafe_allow_html=True)
        god = Image.open('godfather.jpg')
        col10.image(god, width = 155)
        col10.markdown("<p style = 'text-align : center;'> 1.717.256 votes </p>", unsafe_allow_html=True)
        col10.markdown("<p style = 'text-align : center;'> Note moyenne: 9.2 </p>", unsafe_allow_html=True)
        
        top10 = top100_df_bis[:10]
        top10 = top10.sort_values('numVotes', ascending = False)
        fig = px.bar(top10, x='numVotes',
                    y= 'primaryTitle',
                        title = 'Top 10 des films', color_discrete_sequence=['rgb(237,100,90)'], template= 'plotly', hover_name = 'averageRating',
                        )
        fig.update_layout(title= {'x' : 0.5}, hoverlabel=dict(bgcolor="white"))
        fig.update_xaxes(title_text = '')
        fig.update_yaxes(title_text = '')
        st.plotly_chart(fig, use_container_width=True)
        st.write('Le film le plus et le mieux noté est The Shawshank Redemption')
        
    if option == 'Les genres':
        st.subheader('Les genres')
        
        st.write('Le genre principal le plus représenté parmis les films est Drame, suivi par les comédies et les documentaires.')
        fig = px.histogram(movie_rating, x='genre 1',
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
        fig = px.histogram(actors, x='age_fork', color = 'category',
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
        
        movies_vote_genre = top100_df_bis.pivot_table(index='genre 1', values='numVotes',aggfunc='sum')
        movies_vote_genre.sort_values(by='numVotes', ascending = False)
        movies10_vote_genre = movies_vote_genre.sort_values(by='numVotes', ascending = False)[:10]
        fig = px.bar(x=movies10_vote_genre.index,
                    y =movies10_vote_genre['numVotes'],
                        title = 'Nombre de votes par genre', color_discrete_sequence=['rgb(249,166,166)'], template= 'plotly')
        fig.update_layout(title= {'x' : 0.5}, hoverlabel=dict(bgcolor="white"))
        fig.update_xaxes(title_text = '')
        fig.update_yaxes(title_text = '')
        movie_col.plotly_chart(fig, use_container_width=True)
        
        movies_rating_genre = top100_df_bis.pivot_table(index='genre 1', values='averageRating')
        movies_rating_genre = movies_rating_genre.sort_values(by='averageRating', ascending = False)[:10] 
        fig = px.bar(x=movies_rating_genre.index,
                    y =movies_rating_genre['averageRating'],
                        title = 'Moyenne des notes des films par genre', color_discrete_sequence=['rgb(237,100,90)'], template= 'plotly')
        fig.update_layout(title= {'x' : 0.5}, hoverlabel=dict(bgcolor="white"))
        fig.update_xaxes(title_text = '')
        fig.update_yaxes(title_text = '')
        serie_col.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        top_actors = top_100_actors['primaryName'].value_counts()[:10]
        
        col1.write('Quels sont les acteurs les plus présents dans ce top 100 ?')
        fig = px.bar(x=top_actors.index,
                    y = top_actors.values,
                        title = 'Les 10 acteurs les plus présents dans le top 100 des films', color_discrete_sequence=['rgb(237,100,90)'], template= 'plotly')
        fig.update_layout(title= {'x' : 0.5}, hoverlabel=dict(bgcolor="white"))
        fig.update_xaxes(title_text = '')
        fig.update_yaxes(title_text = '')
        col1.plotly_chart(fig, use_container_width=True)
        col1.write('9 acteurs sur 10 dans le top 100 sont des hommes. Leonardo DiCaprio et Robert Downey JR. sont présents dans 7 films du top.')
        
        
        top_real = top_real_df['primaryName'].value_counts()[:10]
        col2.write('Quels sont les réalisateurs les plus présents dans ce top 100 ?')
        fig = px.bar(x=top_real.index,
                    y = top_real.values,
                        title = 'Les 10 réalisateurs les plus présents dans le top 100 des films', color_discrete_sequence=['rgb(249,166,166)'], template= 'plotly')
        fig.update_layout(title= {'x' : 0.5}, hoverlabel=dict(bgcolor="white"))
        fig.update_xaxes(title_text = '')
        fig.update_yaxes(title_text = '')
        col2.plotly_chart(fig, use_container_width=True)
        col2.write('Christopher Nolan a réalisé 7 films du top 100 et arrive premier de ce classement. Nous retrouvons également avec 5 films dans le classement : Martin Scorsese, Steven Spielberg et Tanrantino.')
        
        top_decade = top100_df_bis['decade'].value_counts()
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
        
        
        
    