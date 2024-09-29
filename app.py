import streamlit as st
import pydeck as pdk
import pandas as pd

from globals import KPI
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


def fetch_lat_long(qualifier):

    entity_data = get_entity_data(qualifier)

    return (
        entity_data.get('latitude', None),
        entity_data.get('longitude', None),
        entity_data.get('img_url', None)
    )


if __name__ == "__main__":

    logo = load_resources()

    st.sidebar.write("<h1> Euskadi </h1> ", unsafe_allow_html=True)
    st.sidebar.write(logo, unsafe_allow_html=True)
    st.sidebar.markdown(
        "[https://opendata.euskadi.eus](https://opendata.euskadi.eus)")

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
                filtered_municipios['Latitud'], filtered_municipios['Longitud'], filtered_municipios["Image URL"] = zip(
                    *filtered_municipios['Qualifier'].apply(fetch_lat_long))

            st.write(f"Numero de municipios de : {len(filtered_municipios)}")
            st.write(filtered_municipios)

            show_municipios(filtered_municipios)

            selected_municipio_info = st.selectbox("Mas información", selected_municipio)


            if selected_municipio_info:
                municipios_dict = filtered_municipios.set_index('Municipio').to_dict('index')

                info = municipios_dict[selected_municipio_info]
                st.write(info)
                
                data = KPI.get_inidicators(info["ID"])

                st.json(data)
                with st.spinner('Cargando imagen'):
                    st.image(info["Image URL"], caption=selected_municipio_info,
                                use_column_width=True)
             
