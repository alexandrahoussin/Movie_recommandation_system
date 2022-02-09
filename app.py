import home
import eda
import reco
import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

# nos pages
PAGES = {
    "Home" : home,
    "Exploration des données" : eda,
    "Recommandations de films" : reco
}

# menu sur le côté pour navigation entre les pages
logo = Image.open('NOTFLIX.png')
st.sidebar.image(logo)
st.sidebar.title('Menu')
selection = st.sidebar.selectbox('Quelle page souhaitez-vous visiter?', list(PAGES.keys()))
page = PAGES[selection]
page.app()


st.sidebar.title('A propos')
st.sidebar.info(
    "Cette application a été créée par: "
)

layout = st.sidebar.columns(3)
with layout[0]:
    
    st.write('[Mathis Grassot](https://github.com/Mathis-GrSsT)')
with layout[1]:
    
    st.write('[Alexandra Houssin](https://github.com/alexandrahoussin)')
with layout[2]:
    
    st.write('[Thomas Hamel](https://github.com/TomasHamel)') 


    
    