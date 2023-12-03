# Importar Bibliotecas ------------------------------------------------------------------------------------------------------

import streamlit as st
import streamlit_folium
import base64

# Data manipulation 

import pandas as pd
import numpy as np

# Data Visualization

import matplotlib.pyplot as plt
import seaborn as sns
import folium 

# Warnings 

import warnings
warnings.filterwarnings('ignore')

# Load data
#demand_2023 = pd.read_csv('data/prediccion2023.csv')
#data2 = pd.read_csv('data/nomenclatura_2023_09.csv', encoding='ISO-8859-1')

st.set_page_config(
    page_title="Rebalanceo MiBici 2023",
    page_icon="🚲"
)

#st.markdown('images/miBici.gif',unsafe_allow_html = True)
#st.image("images/miBici.gif", caption = 'Este proyecto se realizó con datos abiertos de MiBici', use_column_width=True)

st.title("Rebalanceo de bicicletas en estaciones de MiBici en 2023")

@st.cache_data  # Caché para acelerar la lectura de datos

def cargar_datos(nombre_archivo, encoding):
    data = pd.read_csv(nombre_archivo, encoding=encoding)
    return data

archivo1 = 'data/prediccion2023.csv'
demand_2023 = cargar_datos(archivo1, encoding='utf-8')

archivo2 = 'data/nomenclatura_2023_09.csv'
data2 = cargar_datos(archivo2, encoding='ISO-8859-1')


data2 = data2.loc[data2['status'] == 'IN_SERVICE']
data2.reset_index(inplace=True)
estaciones = list(data2.id)

# Function to calculate ideal bikes
def bikes_per_station(demanda):
    bikes = 0
    flow = 0

    for d in demanda:
        flow += d

        if flow < 0:
            bikes += abs(flow)
            flow = 0

    return bikes

# Function to calculate ideal bikes for a station, month, and day
def rebalanceo(station, month, day, demand_2023):
    ideal_bikes_df = pd.DataFrame()

    ideal_bikes_df['Estación'] = [station]
    ideal_bikes_df['Periodo 1: 00:00 hrs'] = [bikes_per_station(demand_per_day(station, month, day, period=1, demand_2023=demand_2023))]
    ideal_bikes_df['Periodo 2: 12:00 hrs'] = [bikes_per_station(demand_per_day(station, month, day, period=2, demand_2023=demand_2023))]
    ideal_bikes_df['Periodo 3: 19:00 hrs'] = [bikes_per_station(demand_per_day(station, month, day, period=3, demand_2023=demand_2023))]

    return ideal_bikes_df

# Function to get demand per day
def demand_per_day(station, month, day, period, demand_2023):
    estacion_df = demand_2023.loc[demand_2023['Station'] == station]

    estacion_df['Hour'] = pd.to_datetime(estacion_df['Hour'])

    grouped_month = demand_2023.groupby(estacion_df['Hour'].dt.month)

    month_n = grouped_month.get_group(month)

    month_n['Hour'] = pd.to_datetime(month_n['Hour'])

    grouped_day = month_n.groupby(month_n['Hour'].dt.day)
    day_n = grouped_day.get_group(day)

    day_n = pd.concat([day_n.iloc[list(range(5, 24))], day_n.iloc[[0]]])

    demanda_total = list(map(int, list(day_n['Count'])))

    if period == 1:
        return demanda_total[:7]
    elif period == 2:
        return demanda_total[7:15]
    elif period == 3:
        return demanda_total[15:]

# Streamlit App
def main():
    
    mensaje_inicial = st.empty()
    
    mensaje_inicial.subheader("Presiona el botón: 'Generar Resultados' en el menú de parámetros para generar la información")
    
    traduccion = {'Enero':1, 
                  'Febrero':2, 
                  'Marzo':3, 
                  'Abril':4, 
                  'Mayo':5, 
                  'Junio':6, 
                  'Julio':7, 
                  'Agosto':8, 
                  'Septiembre':9,
                 'Octubre':10, 
                  'Noviembre':11,
                 'Diciembre':12}
    
    mes = st.sidebar.selectbox('Selecciona el mes:', ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre','Octubre' ,'Noviembre','Diciembre' ])
    
    month = traduccion[mes]
    
    day = st.sidebar.slider('Select Day', 1, 31, 1)
    
    if st.sidebar.button('Generar Resultados'):
        mensaje_inicial.empty()
        col1, col2 = st.columns(2)
        
        with col1:

            dia_ideal = pd.DataFrame()

            t = len(estaciones) - 1
            for i, estacion in enumerate(estaciones):
                dia_ideal = pd.concat([dia_ideal, rebalanceo(estacion, month, day, demand_2023)])

            dia_ideal.reset_index(inplace=True)
            dia_ideal.drop(columns=dia_ideal.columns[0], axis=1, inplace=True)

            dia_ideal_mapa = pd.concat([dia_ideal, data2[['latitude', 'longitude']]], axis=1)
            
            dia_ideal_mapa[dia_ideal_mapa.columns[:4]]

            # Create a folium map
            m = folium.Map(location=(20.66682, -103.39182), zoom_start=12)
            #marker_cluster = MarkerCluster().add_to(m)

            icon_path = 'data/bike1.ico'

            for i in range(len(dia_ideal_mapa['latitude'])):
                lat = dia_ideal_mapa['latitude'][i]
                lon = dia_ideal_mapa['longitude'][i]
                info = dia_ideal_mapa[['Estación', 'Periodo 1: 00:00 hrs',
                                       'Periodo 2: 12:00 hrs',
                                       'Periodo 3: 19:00 hrs']].loc[i]

                info_html = pd.DataFrame(info).T.to_html(classes='table table-striped table-hover table-condensed table-responsive')
                custom_icon = folium.CustomIcon(
                    icon_image=icon_path,
                    icon_size=(30, 30)
                )

                popup = folium.Popup(html=info_html, max_width=300)

                mark = folium.Marker(location=(lat, lon), popup=popup, icon=custom_icon)
                mark.add_to(m)

            # Display the map in Streamlit
            streamlit_folium.folium_static(m, width=800, height=600)
            
        with col2:
            file_ = open("data/miBici.gif", "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()

            # Especificar el ancho y alto deseados en píxeles
            width = 300  # Ancho deseado
            height = 200  # Alto deseado

            # Usar la etiqueta HTML para mostrar el GIF con el estilo especificado
            st.markdown(
                f'<img src="data:image/gif;base64,{data_url}" alt="miBici" width={width} height={height} style="display: block; margin: 0 auto; text-align: center;">',
                unsafe_allow_html=True
            )

    # Notas
    st.sidebar.info("Esta aplicación permite calcular el número óptimo de bicicletas que necesitan las estaciones del servicio MiBici en Jalisco para hacer un rebalanceo durante tres horarios en un día determinado durante 2023.")
    # Créditos y fuente de datos
    st.sidebar.subheader("Sígueme en Github: 👇")

    st.sidebar.write("[manuelsolan_o](https://github.com/manuelsolan-o)")

if __name__ == '__main__':
    main()
