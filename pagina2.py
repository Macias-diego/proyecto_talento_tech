#-------------------------Mix Electrico-----------------------------------
#librerias
import streamlit as st
import json
from modules.data_load import *
from modules.data_cleaning import *
from modules.data_analysis import *

#------------------------DATOS-------------------------------------
with open('data.json', 'r') as f:
  Paises_from_json = json.load(f)

Paises = {key: pd.DataFrame(data) for key, data in Paises_from_json.items()}
#-----------------------------------------------------------------
#--------------------------app----------------------------------------
st.set_page_config(layout="wide")

#Titulo, se usa st.markdown para mayor estetica,
#la otra opcion es: st.title(f"Evolución de la generación de energía electrica y Emisiones de CO2")
st.markdown("""
        <style>
        .title-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100px; /* puedes reducirlo si quieres más arriba */
            margin-top: -40px; /* sube el título */
            margin-bottom: 20px;
        }
        .title-text {
            font-size: 40px;
            font-weight: bold;
            text-align: center;
        }
        </style>

        <div class="title-container">
            <div class="title-text">Mix de Energía eléctrica</div>
        </div>
            """, unsafe_allow_html=True)
#-----------------------------------------------------------
st.sidebar.header('Filtros para la evolución del mix eléctrico')
paises_seleccionados=st.sidebar.multiselect('Seleccione los paises',list(Paises.keys()),
                                        key='pais1',
                                        placeholder="Elige un pais para analizar",
                                        default=['Colombia','Latinoamerica'], 
                                        max_selections=2,
                                        accept_new_options=True)
    
    #Selección de rango de años
desde_año, hasta_año = st.sidebar.slider(
        'Cuales años te interesan?',
        min_value=1985,
        max_value=2023,
        value=[1985, 2023])

st.sidebar.header('Filtros para el mix eléctrico de un año en especifico')

fuentes_de_energia = {'Solar':"Generacion solar [TWh]",
                          'Eólica':"Generacion eolica [TWh]",
                          'Geotérmica y Biomasa':"Generacion geotermica-biomasa-otras [TWh]",
                          'Hidro':"Generacion hidroelectrica [TWh]",
                          'Renovables':"Generacion renovable con hidroelectrica [TWh]",
                          'Renovables sin Hidro':"Generacion renovable sin hidroelectrica [TWh]",
                          'No renovable':"Generacion no renovable [TWh]"}
 

año=st.sidebar.selectbox('Año a analizar a profundidad: ', np.arange(2023,1985,-1))


variables_seleccionadas = st.sidebar.pills('Seleccione las fuentes de generacion energetica',
                                       list(fuentes_de_energia.keys()), 
                                       selection_mode="multi",
                                       default=['Solar','Eólica','Geotérmica y Biomasa','Hidro','No renovable'],
                                       label_visibility="collapsed"
                                       )


st.header('Evolución historica del mix eléctrico')
st.write('''
         Se tiene que tanto en Colombia como América Latina presentan un claro potencial de transformación hacia una matriz energética más diversificada y sostenible. 
         Históricamente, la energía hidroeléctrica ha sido la base de la generación renovable en ambas regiones. Sin embargo, la creciente preocupación por 
         la fiabilidad de la hidroeléctrica, debido a factores como el cambio climático y la variabilidad hídrica, impulsa la necesidad de adoptar otras fuentes 
         de energía.Los datos revelan un crecimiento significativo, aunque reciente, en la generación de energía eólica y solar. 
         Esto indica que estas fuentes están ganando impulso y demostrando su capacidad para complementar y eventualmente reducir la dependencia de la energía 
         hidroeléctrica. 
         ''')

col1, col2 =st.columns([1,1])

with col1: 
    if  paises_seleccionados==[]:
        st.write('(Escoge un pais para poder graficar)')
    else:
        fig2=grafico_matriz_energetica_bar(Paises[paises_seleccionados[0]],paises_seleccionados[0],desde_año,hasta_año)
        st.pyplot(fig2)
    
with col2:
    if  paises_seleccionados==[] or len(paises_seleccionados)==1:
        st.write('(Escoge un pais para poder graficar)')
    else:
        fig4=grafico_matriz_energetica_bar(Paises[paises_seleccionados[1]],paises_seleccionados[1],desde_año,hasta_año)
        st.pyplot(fig4)

st.write('''
         Tanto en Colombia como en Latinoamérica la generación total de energía ha aumentado sostenidamente desde 1985, 
         pero con diferencias en la composición de las fuentes. En Colombia, la generación sigue dominada por la hidroeléctrica, 
         con un crecimiento lento de otras renovables a partir de 2015. En cambio, en Latinoamérica, aunque la hidroeléctrica también es importante, 
         se observa una mayor diversificación con un aumento notable de las energías renovables no hidráulicas desde 2010. Esto indica que la región 
         avanza más rápido hacia una matriz energética más diversificada y sostenible que Colombia.
         ''')

col1, col2 =st.columns([1,1])

with col1: 
    if  paises_seleccionados==[]:
        st.write('(Escoge un pais para poder graficar)')
    else:
        fig1=grafico_tiempo(Paises[paises_seleccionados[0]],["Generacion total de energia  [TWh]","Hidro","Renovables sin Hidro","No renovable"],desde_año,hasta_año,paises_seleccionados[0])
        st.pyplot(fig1)
    
with col2:
    if  paises_seleccionados==[] or len(paises_seleccionados)==1:
        st.write('(Escoge un pais para poder graficar)')
    else:
        fig3=grafico_tiempo(Paises[paises_seleccionados[1]],["Generacion total de energia  [TWh]","Hidro","Renovables sin Hidro","No renovable"],desde_año,hasta_año,paises_seleccionados[1])
        st.pyplot(fig3)

st.header(f'Análisis profundo del Año {año}')


if paises_seleccionados==[] or len(paises_seleccionados)==1:
        st.write('(Escoge un pais para poder graficar)')
else:
    mostrar_kpis_comparativos(Paises[paises_seleccionados[0]],Paises[paises_seleccionados[1]],año)

    if variables_seleccionadas==[]:
        st.write('(Escoge fuentes de energia para graficar)')
    else:
        fig1=grafico_barras_agrupadas(paises_seleccionados,año,año,variables_seleccionadas,Paises)
        st.pyplot(fig1)


