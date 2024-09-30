import streamlit as st
import pydeck as pdk
import pandas as pd
import plotly.express as px


from globals import API_KPI
from wikiData import get_entity_data
from linkedData import load_municipios
from resourceManager import load_resources


def show_municipios(df):

    scatterplot_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[Longitud, Latitud]',
        get_fill_color='[30, 144, 255, 160]',
        get_radius=2000,  # Size of each point
        radius_scale=1,
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=df['Latitud'].mean(),
        longitude=df['Longitud'].mean(),
        zoom=10,
        pitch=0,
    )

    r = pdk.Deck(
        layers=[scatterplot_layer],
        initial_view_state=view_state,
        tooltip={"text": f"{{Hospital}}: {{{0}}}"},
    )

    st.pydeck_chart(r)


def show_indicator(years_data, selected_indicator):

    fig = px.line(years_data, x='Year', y='Value', title=f'{selected_indicator}')

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Value",
        template="plotly_white"  
    )

    st.plotly_chart(fig)

    
def fetch_lat_long(qualifier):

    entity_data = get_entity_data(qualifier)

    return (
        entity_data.get('latitude', None),
        entity_data.get('longitude', None),
        entity_data.get('img_url', None)
    )

def search_municipality():

    df_municipios = load_municipios()
    seleteted_provincia = st.multiselect(
        'Elige una provincia:', df_municipios['Provincia'].unique())

    if seleteted_provincia:
        filtered_municipios = df_municipios[df_municipios['Provincia'].isin(
            seleteted_provincia)]

        selected_municipio = st.multiselect(
            'Elige un Municipio:', filtered_municipios['Municipio'])

        if selected_municipio:
            filtered_municipios = df_municipios[df_municipios['Municipio'].isin(
                selected_municipio)]

            with st.spinner('Cargando información de los municipios'):

                lat_long_pairs = filtered_municipios['Qualifier'].apply(
                    fetch_lat_long)

                latitudes, longitudes, image_urls = zip(*lat_long_pairs)

                filtered_municipios[['Latitud', 'Longitud', 'Image URL']] = pd.DataFrame({
                    'Latitud': latitudes,
                    'Longitud': longitudes,
                    'Image URL': image_urls
                })


            st.write(f"Numero de municipios de : {len(filtered_municipios)}")
            st.write(filtered_municipios)

            show_municipios(filtered_municipios)

            selected_municipio_info = st.selectbox(
                "Mas información", selected_municipio)

            if selected_municipio_info:
                municipios_dict = filtered_municipios.set_index(
                    'Municipio').to_dict('index')

                info = municipios_dict[selected_municipio_info]
                
                #st.write(info)

                with st.spinner('Cargando imagen'):
                    st.image(info["Image URL"], caption=selected_municipio_info,
                             use_column_width=True)
                    
                data = API_KPI.get_inidicators(info["ID"])

                #st.json(data)

                indicator_names = [indicator['name'] for indicator in data['indicators']]
            
                selected_indicator = st.selectbox("Selecciona un Indicador", indicator_names)

                for indicator in data['indicators']:
                    if indicator['name'] == selected_indicator:
                        
                        years_data = pd.DataFrame(indicator['years'][0].items(), columns=['Year', 'Value'])

                        show_indicator(years_data, selected_indicator)

                        links = indicator['_links']
                        st.write(f"**More Info:** [Link to indicator]({links['self']['href']})")
                


if __name__ == "__main__":

    logo = load_resources()

    st.sidebar.write(
        "<h1> Bizileku Bila </h1>  <h2><i>En busca de un lugar para vivir en Euskadi</i> </h2> ", unsafe_allow_html=True)
    st.sidebar.write(logo, unsafe_allow_html=True)
    st.sidebar.markdown(
        "[https://opendata.euskadi.eus](https://opendata.euskadi.eus)")

    search_municipality()
