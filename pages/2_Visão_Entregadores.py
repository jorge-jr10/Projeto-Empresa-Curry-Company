# libraries
from haversine import haversine
import plotly.express as px 
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
from PIL import Image
import folium 
from streamlit_folium import folium_static
import pandas as pd

#usando a largura total da página no streamlit
st.set_page_config(page_title='Visão entregadores', layout='wide')

#funções
def top_delivers(df1, top_asc):
                df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
                                                     .groupby(['City', 'Delivery_person_ID'])
                                                     .max()
                                                     .sort_values(['City', 'Time_taken(min)'], ascending=top_asc)
                                                     .reset_index())
            
                df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
                df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
                df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

                df3 = pd.concat( [df_aux01, df_aux02, df_aux03] ).reset_index( drop=True )

                return df3

def clean_code(df1):
        
    # 1. convertendo a coluna Age de texto para número e removendo "NaN "
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    # 2. removendo 'NaN' da coluna Road_traffic_density, City e Festival
    linhas_selecionadas = (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['Festival'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    # 3. convertendo a coluna Ratings de texto para numero decimal (float)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

    # 4. convertendo a coluna Order_Date de texto para data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

    # 5. convertendo multiples_deliveries de texto para numero inteiro (int) / removendo 'NaN ' 
    linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, : ].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

    # 6. removendo os espaços dentro de strings
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    # 7. limpando a coluna time taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(str)
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.replace('(min)', '').strip())
    def safe_int_conversion(x):
        if x.isdigit():  
            return int(x)
        else:
            try:
                return int(float(x))
            except ValueError:
            
                return None
            
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(safe_int_conversion)

    return df1


# import dataset 
df = pd.read_csv('pages/dataset/train.csv')

#limpando o dataset
df1 = clean_code( df )


#=====================================
# Barra lateral no Streamlit
#=====================================
st.header('Marketplace - Visão Entregadores')

image = Image.open('target.png')
st.sidebar.image( image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest delivery in Town')
st.sidebar.markdown("---")

st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=datetime.strptime('2022-03-07', '%Y-%m-%d'),
    min_value=datetime.strptime('2022-02-11', '%Y-%m-%d'),
    max_value=datetime.strptime('2022-04-06', '%Y-%m-%d'),
    format='DD-MM-YYYY')

st.sidebar.markdown("---")


traffic_options = st.sidebar.multiselect(
    'Selecione as condições de trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam']
)

st.sidebar.markdown("---")

st.sidebar.markdown("## Powered by Jorge Junior ")

#filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

#filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]


#=====================================
# Layout no Streamlit
#=====================================

tab1, = st.tabs(['Visão Geral'])

with tab1: 
    with st.container():
        st.title(' Métricas gerais ' )
        col1, col2, col3, col4 = st.columns(4, gap='Large')
        with col1:
            #maior idade entre os entregadores
            maior_idade = (df1.loc[:, 'Delivery_person_Age'].max())
            col1.metric('Maior idade', maior_idade)

        with col2:
            #menor idade entre os entregadores
            menor_idade = (df1.loc[:, 'Delivery_person_Age'].min())
            col2.metric('Menor idade', menor_idade)
                        
        with col3:
            #menor condição de veículo
            melhor_condicao = format(df1.loc[:, 'Vehicle_condition'].max())
            col3.metric('Melhor condição', melhor_condicao)

        with col4:
            #menor condição de veículo
            pior_condicao = format(df1.loc[:, 'Vehicle_condition'].min())
            col4.metric('Pior condição', pior_condicao)

    
    with st.container():
        st.markdown("---")
        st.title( 'Avaliações' )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Média de avaliações por entregador')
            # removendo os valores 'NaN' para realizar a média
            df = df1[df1['Delivery_person_Ratings'] != 'NaN ']
                                        
            avg_ratings_per_delivery = (df.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
                                                        .groupby( 'Delivery_person_ID' )
                                                        .mean()
                                                        .reset_index() )
        
            st.dataframe(avg_ratings_per_delivery)

        with col2:
            st.markdown('##### Avaliação média e desvio padrão por densidade de trânsito')
            df_avg_std_rating_by_traffic = (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                                                        .groupby('Road_traffic_density')
                                                        .agg({'Delivery_person_Ratings': [ 'mean', 'std' ]})    
                                                        .reset_index())

            # mudança do nome das colunas
            df_avg_std_rating_by_traffic.columns = ['Road_traffic_density', 'delivery_mean', 'delivery_std']

            st.dataframe(df_avg_std_rating_by_traffic)


            st.markdown('##### Avaliação média e desvio padrão por clima')
            df_avg_std_rating_by_traffic = ((df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                                                        .groupby('Weatherconditions')
                                                        .agg({'Delivery_person_Ratings': [ 'mean', 'std' ]})
                                                        .reset_index()))

            # mudança do nome das colunas
            df_avg_std_rating_by_traffic.columns = ['Weatherconditions', 'delivery_mean', 'delivery_std']

            st.dataframe(df_avg_std_rating_by_traffic)

    with st.container():
        st.markdown("---")
        st.title('Velocidade de entrega')

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('##### Top entregadores mais rápidos por cidade')
            df3 = top_delivers(df1, top_asc=True)
            st.dataframe(df3)

        with col2:
            st.markdown('##### Top entregadores mais lentos por cidade')
            df3 = top_delivers(df1, top_asc=False)
            st.dataframe(df3)           
