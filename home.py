import streamlit as st
from PIL import Image



def app():
    col1, col2, col3 = st.columns(3)
    logo = Image.open('NOTFLIX.png')
    col2.image(logo)
    col2.markdown("<h1 style = 'text-align : center'> Bienvenue sur Notflix ! </h1>", unsafe_allow_html=True)

    
    col2.write("Notflix est l'app que nous avons crée pour notre projet de datascience avec la Wild Code School.")
    col2.markdown("Un cinéma en perte de vitesse dans la Creuse a besoin de nous pour sa transition **digitale**. Il nous demande de créer un moteur de recommandations de films.")
    col2.markdown("Nous sommes dans une situation de cold start, aucun client n'a renseigné ses préférences. Nous n'avons à disposition que les bases de données du célèbre site [IMDB](https://datasets.imdbws.com/).")
    col2.markdown("Pour pouvoir fournir ce que le client souhaitait, nous avons commencé par une exploration des bases de données. Cette exploration a faire ressortir plusieurs tendances qui nous ont permis d'affiner nos idées pour le moteur de recommandations.")
    col2.markdown("Nous avons donc développé un modèle de machine learning à partir d'un algorithme de Nearest Kneighbors. Pour résumer, l'algo tente de recommander un (ou plusieurs) film(s) similaire(s) au film que l'user a aimé précédemment. ")
    col2.markdown("Et enfin, il a vu le jour... ce fameux moteur de recommandations de films ! On vous laisse juger par vous-même...")
    
    
    
    