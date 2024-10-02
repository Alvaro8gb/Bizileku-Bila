
import streamlit as st
import pydeck as pdk
import pandas as pd
import plotly.express as px


from globals import API_KPI
from wikiData import get_entity_data
from linkedData import load_municipios
from resourceManager import load_resources
from models import create_indicators


@st.cache_data
def show_municipios(df):

    scatterplot_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position="[Longitud, Latitud]",
        get_fill_color="[30, 144, 255, 160]",
        get_radius=2000,  # Size of each point
        radius_scale=1,
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=df["Latitud"].mean(),
        longitude=df["Longitud"].mean(),
        zoom=9,
        pitch=0,
    )

    r = pdk.Deck(
        layers=[scatterplot_layer],
        initial_view_state=view_state,
        tooltip={"text": f"{{Hospital}}: {{{0}}}"},
    )

    st.pydeck_chart(r)


@st.cache_data
def show_indicator(years_data, selected_indicator):

    fig = px.line(years_data, x="Año", y="Valor",
                  title=f"{selected_indicator}")

    fig.update_layout(xaxis_title="Año", yaxis_title="Valor",
                      template="plotly_white")

    st.plotly_chart(fig)


@st.cache_data
def fetch_lat_long(qualifier):

    entity_data = get_entity_data(qualifier)

    return (
        entity_data.get("latitude", None),
        entity_data.get("longitude", None),
        entity_data.get("img_url", None),
    )


def select_groups(indicators_dict: dict):
    groups = list(
        set(
            [
                indicator.group
                for indicator in indicators_dict.values()
            ]
        )
    )

    selected_group = st.selectbox("Selecciona un Grupo", groups)

    filtered_subgroups = list(
        set(
            indicator.subgroup
            for indicator in indicators_dict.values()
            if indicator.group == selected_group
        )
    )

    selected_subgroup = st.selectbox(
        "Selecciona un Subgrupo", filtered_subgroups
    )

    filtered_indicators = [
        indicator.name
        for indicator in indicators_dict.values()
        if indicator.subgroup == selected_subgroup
    ]

    return filtered_indicators


def select_indicator_one(indicators_dict: dict):

    filtered_indicators = select_groups(indicators_dict)

    selected_indicator = st.selectbox(
        "Selecciona un Indicador", filtered_indicators
    )

    indicator = indicators_dict[selected_indicator]

    return indicator


def select_indicator_several(indicators_json: dict):

    indicators_dict = create_indicators(indicators_json)

    filtered_indicators = select_groups(indicators_dict)

    selected_indicators_names = st.multiselect(
        "Selecciona un Indicador", filtered_indicators
    )

    indicators = [indicators_dict[name] for name in selected_indicators_names]

    return indicators


def search_municipality():

    df_municipios = load_municipios()
    seleteted_provincia = st.multiselect(
        "Elige una provincia:", df_municipios["Provincia"].unique()
    )

    if seleteted_provincia:
        filtered_municipios = df_municipios[
            df_municipios["Provincia"].isin(seleteted_provincia)
        ]

        selected_municipio = st.multiselect(
            "Elige un Municipio:", filtered_municipios["Municipio"]
        )

        if selected_municipio:
            filtered_municipios = df_municipios[
                df_municipios["Municipio"].isin(selected_municipio)
            ]

            with st.spinner("Cargando información de los municipios"):

                lat_long_pairs = filtered_municipios["Qualifier"].apply(
                    fetch_lat_long)

                latitudes, longitudes, image_urls = zip(*lat_long_pairs)

                filtered_municipios.loc[:, "Latitud"] = latitudes
                filtered_municipios.loc[:, "Longitud"] = longitudes
                filtered_municipios.loc[:, "Image URL"] = image_urls

            st.write(f"Numero de municipios de : {len(filtered_municipios)}")
            # st.write(filtered_municipios)

            show_municipios(filtered_municipios)

            selected_municipio_info = st.selectbox(
                "Mas información", selected_municipio
            )

            if selected_municipio_info:
                municipios_dict = filtered_municipios.set_index("Municipio").to_dict(
                    "index"
                )

                info = municipios_dict[selected_municipio_info]

                # st.write(info)

                with st.spinner("Cargando imagen"):
                    st.image(
                        info["Image URL"],
                        caption=selected_municipio_info,
                        use_column_width=True,
                    )

                indicators_json = API_KPI.get_inidicators(info["ID"])

                #st.json(indicators_json)

                indicators_dict = create_indicators(indicators_json["indicators"])
                indicator = select_indicator_one(indicators_dict)

                years_data = pd.DataFrame(
                    list(indicator.years.items()), columns=["Año", "Valor"]
                )

                if years_data.empty:
                    st.write("No hay datos para este indicador")
                elif years_data.shape[0] == 1:
                    st.write(f"{indicator.name}")
                    years_data.set_index("Año", drop=False, inplace=True)
                    years_data.drop(columns=["Año"], inplace=True)
                    st.table(years_data)
                else:
                    show_indicator(years_data, indicator.name)


def find_municipality():

    indicators_json = API_KPI.get_all_indicators()

    st.json(indicators_json)
    indicators = select_indicator_several(indicators_json)


if __name__ == "__main__":

    logo = load_resources()

    st.sidebar.write(
        "<h1> Bizileku Bila </h1>  <h2><i>En busca de un lugar para vivir en Euskadi</i> </h2> ",
        unsafe_allow_html=True,
    )
    st.sidebar.write(logo, unsafe_allow_html=True)
    st.sidebar.markdown(
        "[https://opendata.euskadi.eus](https://opendata.euskadi.eus)")

    st.sidebar.title("Navegación")
    selected_section = st.sidebar.radio(
        "Elige una sección:",
        [
            "Encontrar tu municipio para vivir",
            "Ver toda la informacion de un municipio",
        ],
    )

    if selected_section == "Encontrar tu municipio para vivir":
        st.header("Section: ncontrar tu municipio para vivir")
        st.write("This section provides an overview of the data.")
        find_municipality()

    elif selected_section == "Ver toda la informacion de un municipio":
        st.header("Section: Ver toda la informacion de un municipio")
        st.write("This section provides analysis on the data.")
        search_municipality()
    else:
        pass
