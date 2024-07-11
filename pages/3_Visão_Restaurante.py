# libraries
from haversine import haversine
import plotly.express as px 
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
from PIL import Image
import folium 
from streamlit_folium import folium_static
import numpy as np
import pandas as pd

#usando a largura total da página no streamlit
st.set_page_config(page_title='Visão restaurante', layout='wide')

#funções 
def avg_std_time_graph( df1 ):
            
                colunas = ['City', 'Time_taken(min)']
                df_aux = df1.loc[:, colunas].groupby( 'City' ).agg( {'Time_taken(min)' : ['mean', 'std']} )

                df_aux.columns = ['avg_time', 'std_time']

                df_aux = df_aux.reset_index()

                fig = go.Figure()
                fig.add_trace( go.Bar( name='Control',
                                    x=df_aux['City'],
                                    y=df_aux['avg_time'],
                                    error_y=dict( type='data', array=df_aux['std_time'] ) ) )
            
                fig.update_layout(barmode='group', xaxis_title='Tipo de cidade', yaxis_title='Tempo médio de entrega')

                return fig

def avg_std_time_delivery(df1, festival, op):

                df_aux = (df1.loc[:, ['Time_taken(min)', 'Festival']]
                                                        .groupby( 'Festival' )
                                                        .agg( {'Time_taken(min)' : ['mean', 'std']} ))

                df_aux.columns = ['avg_time', 'std_time']
                df_aux = df_aux.reset_index()
                df_aux = np.round(df_aux.loc[df_aux['Festival'] == festival, op],2)

                return df_aux

def distance(df1):
                colunas = ['Restaurant_latitude', 'Restaurant_longitude', 
                           'Delivery_location_latitude', 'Delivery_location_longitude']

                df1 ['distance'] = df1.loc[:, colunas].apply( lambda x: haversine(
                                                                    ( x['Restaurant_latitude'],  x['Restaurant_longitude']),
                                                                    ( x['Delivery_location_latitude'],  x['Delivery_location_longitude']  )),
                                                                      axis=1)

                avg_distance = np.round(df1['distance'].mean(),2)

                return avg_distance

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

#limpeza do código
df1 = clean_code(df)

#=====================================
# Barra lateral no Streamlit
#=====================================
st.header('Marketplace - Visão Restaurante')

#image_path = 'C:\\Users\\t51269773852\\OneDrive - DIAGNOSTICOS DA AMERICA S.A\\Documentos\\Repos\\portifolio_projetos'
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
        st.title('Métricas Gerais')

        col1, col2, col3, col4, col5, col6 = st.columns( 6 )
        with col1:
            delivery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique())
            col1.metric('Entregadores únicos', delivery_unique )

        with col2:
            avg_distance = distance(df1)
            col2.metric('Distância média', avg_distance)
              
         
        with col3:
            df_aux = avg_std_time_delivery( df1, 'Yes', 'avg_time')
            col3.metric(' Tempo médio', df_aux)

        with col4: 
            df_aux = avg_std_time_delivery( df1, 'Yes', 'std_time')
            col4.metric(' STD Entrega', df_aux)          

        with col5:
            df_aux = avg_std_time_delivery( df1, 'No', 'avg_time')
            col5.metric(' Tempo médio', df_aux)

        with col6:
            df_aux = avg_std_time_delivery( df1, 'No', 'std_time')
            col6.metric(' STD Entrega', df_aux)      

    with st.container():
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1: 
            st.markdown("Tempo médio de entrega por cidade com variabilidade")
            fig = avg_std_time_graph(df1)
            st.plotly_chart(fig)

        with col2:
             st.markdown('Tempo médio de entrega e desvio padrão por cidade e tipo de pedido')
             colunas = ['City', 'Time_taken(min)', 'Type_of_order']
             df_aux = df1.loc[:, colunas].groupby( ['City', 'Type_of_order' ] ).agg( {'Time_taken(min)' : ['mean', 'std']} )

             df_aux.columns = ['avg_time', 'std_time']

             df_aux = df_aux.reset_index()

             st.dataframe(df_aux)
             colunas = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']


    with st.container():
        st.markdown("---")
        st.title('Distribuição de tempo')

        col1, col2 = st.columns( 2 )

        with col1:
            st.markdown('Variação de distância Restaurante x Entrega entre as cidades')
            df1 ['distance'] = df1.loc[:, colunas].apply( lambda x: haversine(
                                                                 ( x['Restaurant_latitude'],  x['Restaurant_longitude']),
                                                                 ( x['Delivery_location_latitude'],  x['Delivery_location_longitude']  )), axis=1)

            avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()

            fig = go.Figure(data=[go.Pie( labels=avg_distance['City'], values=avg_distance['distance'], pull=[0.03 , 0.03, 0.03])])

            st.plotly_chart( fig )
                       

        with col2:
            st.markdown('Média e STD do tempo de entrega por cidade e densidade de trânsito')
            df_aux = (df1.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']]
                                            .groupby( [ 'Road_traffic_density', 'City' ] )
                                            .agg( {'Time_taken(min)' : ['mean', 'std']} ))

            df_aux.columns = ['avg_time', 'std_time']

            df_aux = df_aux.reset_index()

            fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time',
                              color='std_time', color_continuous_scale='RdbU',
                              color_continuous_midpoint=np.average(df_aux['std_time']))
            
            st.plotly_chart( fig )  
