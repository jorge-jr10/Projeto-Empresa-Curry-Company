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
st.set_page_config(page_title='Visão empresa', layout='wide')

#funções
def country_maps(df1):
               
        df_aux = (df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                                        .groupby(['City', 'Road_traffic_density'])
                                        .median()
                                        .reset_index())
        map = folium.Map()

        for index, location_info in df_aux.iterrows():
            folium.Marker( [location_info['Delivery_location_latitude'],
                    location_info['Delivery_location_latitude']],
                    popup=location_info[['City', 'Road_traffic_density']]).add_to( map )

        folium_static( map, width=820, height= 600 )

def order_share_by_week(df1):
            
            df_aux01 = (df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year')
                                                          .count()
                                                          .reset_index())
            
            df_aux02 = (df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year')
                                                                          .nunique()
                                                                          .reset_index())

            df_aux = pd.merge( df_aux01, df_aux02, how='inner' )
            df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']

            fig = px.line(df_aux, x='week_of_year', y='order_by_deliver')

            # Remove os títulos dos eixos
            fig.update_layout(xaxis_title='', yaxis_title='Entregador')
            
            return fig 

def order_by_week(df1):
            
            #criar a coluba "Semana"
            df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U' )

            df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()

            fig = px.line( df_aux, x='week_of_year', y='ID' )

            # Remove os títulos dos eixos
            fig.update_layout(xaxis_title='', yaxis_title='')

            return fig

def traffic_order_city(df1):
                df_aux = (df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby( ['City', 'Road_traffic_density'])
                                                                            .count()
                                                                            .reset_index())
                
                fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size= 'ID', color='City')

                # Remove os títulos dos eixos
                fig.update_layout(xaxis_title='', yaxis_title='')
  
                return fig

def traffic_order_share(df1):
                
                df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
                df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
                df_aux['entregas_percentual'] = df_aux['ID'] / df_aux['ID'].sum()

                fig = px.pie ( df_aux, values='entregas_percentual', names='Road_traffic_density' )

                return fig 

def orders_by_day(df1):
            
            # orders metric
            cols = ['ID', 'Order_Date']

            #selecao de linhas
            df_aux = df1.loc[:, cols].groupby( 'Order_Date' ).count().reset_index()

            # gráfico de barras
            fig = px.bar(df_aux, x='Order_Date', y='ID')

            # Remove os títulos dos eixos
            fig.update_layout(xaxis_title='', yaxis_title='')

            return fig 

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

#=================================== Início da estrutura lógica do código =============================================

# import dataset 
df = pd.read_csv('pages/dataset/train.csv')

# limpando os dados
df1 = clean_code (df)


#=====================================
# Barra lateral no Streamlit
#=====================================
st.header('Marketplace - Visão Empresa')

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

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        st.header('Pedidos por dia')
        fig = orders_by_day(df1)
        st.plotly_chart( fig, use_container_width=True)        

    with st.container():

        col1, col2 = st.columns( 2 )

        with col1:
            fig = traffic_order_share(df1)
            st.markdown('#### Entregas por condições de trafégo')
            st.plotly_chart( fig, use_container_width=True)              
    
        with col2:
            st.markdown('#### Entregas por cidade e condições de tráfego')
            fig = traffic_order_city(df1)
            st.plotly_chart( fig, use_container_width=True)

with tab2:
    with st.container():
        st.header('Pedidos por semana')
        fig = order_by_week(df1)
        st.plotly_chart( fig, use_container_width=True)
         
    
    with st.container():
        st.header('Pedidos semanais por entregador')
        fig = order_share_by_week(df1)
        st.plotly_chart( fig, use_container_width=True)

with tab3:
    st.header('Mapa do país')
    country_maps(df1)
