import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Home',
    page_icon='S2'
)

#image_path = 'C:\\Users\\t51269773852\\OneDrive - DIAGNOSTICOS DA AMERICA S.A\\Documentos\\Repos\\portifolio_projetos'
image = Image.open('target.png')
st.sidebar.image( image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest delivery in Town')
st.sidebar.markdown("---")
st.sidebar.markdown("## Powered by Jorge Junior ")

st.write('# Curry Company Growth Dashboard')

st.markdown(

    """
    Growth Dashboard foi construido para acompanhar as métricas de crescimento de entregadores e restaurantes.
    ### De que maneira enxergar essas informações? 

    - Visão empresa:
        - Visão gerencial: Métricas gerais de comportamento
        - Visão Tática: Indicadores semanais de crescimento
        - Visão Geográfica: Insights de geolocalização
    - Visão entregador: 
        - Acompanhamento dos indicadores semanais de crescimento 
    - Visão restaurante: 
        - Indicadores semanais do crescimento dos restaurantes 
"""
)
