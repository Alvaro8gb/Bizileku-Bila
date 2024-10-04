import streamlit as st
import pydeck as pdk
import pandas as pd
import plotly.express as px


from globals import API_KPI
from wikiData import get_entity_data
from linkedData import load_municipios
from resourceManager import load_resources
from models import create_indicators
from score import calculate_score


@st.cache_data
def show_map_municipios(df):

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
        tooltip={"text": "{Municipio}"},
    )

    st.pydeck_chart(r)


@st.cache_data
def show_indicator(years_data, municipality_name, selected_indicator):

    fig = px.line(
        years_data, x="Año", y="Valor", title="Indicador de " + municipality_name
    )

    fig.update_layout(
        xaxis_title="Año",
        yaxis_title=f"{selected_indicator}",
        template="plotly_white",
        width=1000,
        height=600,
        title_x=0.4,
    )

    st.plotly_chart(fig)


def fetch_lat_long(qualifier):

    entity_data = get_entity_data(qualifier)

    return (
        entity_data.get("latitude", None),
        entity_data.get("longitude", None),
        entity_data.get("img_url", None),
    )


def search_coordinates(df):

    with st.spinner("Cargando información de los municipios"):

        lat_long_pairs = df["Qualifier"].apply(fetch_lat_long)

        latitudes, longitudes, image_urls = zip(*lat_long_pairs)

        df.loc[:, "Latitud"] = latitudes
        df.loc[:, "Longitud"] = longitudes
        df.loc[:, "Image URL"] = image_urls
    return df


def select_groups(indicators_dict: dict):
    groups = list(set([indicator.group for indicator in indicators_dict.values()]))

    selected_group = st.selectbox("Selecciona un Grupo", groups)

    filtered_subgroups = list(
        set(
            indicator.subgroup
            for indicator in indicators_dict.values()
            if indicator.group == selected_group
        )
    )

    selected_subgroup = st.selectbox("Selecciona un Subgrupo", filtered_subgroups)

    filtered_indicators = [
        indicator.name
        for indicator in indicators_dict.values()
        if indicator.subgroup == selected_subgroup
    ]

    return filtered_indicators


def select_indicator_one(indicators_dict: dict):

    filtered_indicators = select_groups(indicators_dict)

    selected_indicator = st.selectbox("Selecciona un Indicador", filtered_indicators)

    indicator = indicators_dict[selected_indicator]

    return indicator


def select_indicator_several(indicators_json: dict):

    indicators_dict = create_indicators(indicators_json)

    filtered_indicators = select_groups(indicators_dict)

    if "selected_indicators" not in st.session_state:
        st.session_state["selected_indicators"] = []

    st.markdown("### 2. Selecciona los indicadores clave")

    st.write("Ten en cuenta que algunos indicadores, como la criminalidad, pueden distorsionar los resultados.")
                    
    st.markdown("Para mejores sugerencias, **evita seleccionar indicadores que representen aspectos negativos**") 

    selected_indicators_names = st.multiselect(
        "Selecciona un Indicador",
        filtered_indicators,
    )

    if st.button("Añadir indicadores"):
        st.session_state["selected_indicators"] = list(
            set(st.session_state["selected_indicators"] + selected_indicators_names)
        )

    if st.session_state["selected_indicators"]:
        selected_indicators_to_remove = st.multiselect(
            "Selecciona un Indicador para eliminar",
            st.session_state["selected_indicators"],
        )

        if st.button("Eliminar Indicadores"):
            st.session_state["selected_indicators"] = [
                indicator
                for indicator in st.session_state["selected_indicators"]
                if indicator not in selected_indicators_to_remove
            ]

        indicators = [
            indicators_dict[name] for name in st.session_state["selected_indicators"]
        ]

        grouped_data = {}

        for i in indicators:
            group = i.group
            subgroup = i.subgroup

            if group not in grouped_data:
                grouped_data[group] = {}
            if subgroup not in grouped_data[group]:
                grouped_data[group][subgroup] = []

            grouped_data[group][subgroup].append(i)

        html_output = "<ul>"
        for group, subgroups in grouped_data.items():
            html_output += f"<li><strong>{group}</strong><ul>"
            for subgroup, items in subgroups.items():
                html_output += f"<li><strong>{subgroup}</strong><ul>"
                for i in items:
                    html_output += f"<li>{i.name}</li>"
                html_output += "</ul></li>"
            html_output += "</ul></li>"
        html_output += "</ul>"

     #   st.markdown("### Lista de Indicadores Seleccionados:")
     #  st.markdown(html_output, unsafe_allow_html=True)

    indicators = [
        indicators_dict[name] for name in st.session_state["selected_indicators"]
    ]

    return indicators


def search_municipality(df_municipios):
    st.subheader("1. Selecciona el municipio que quieres explorar")
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

            # st.write(f"Numero de municipios de : {len(filtered_municipios)}")
            # st.write(filtered_municipios)

            filtered_municipios = search_coordinates(filtered_municipios)

            show_map_municipios(filtered_municipios)

            selected_municipality = st.selectbox("Mas información", selected_municipio)

            if selected_municipality:
                municipios_dict = filtered_municipios.set_index("Municipio").to_dict(
                    "index"
                )

                info = municipios_dict[selected_municipality]

                # st.write(info)

                with st.spinner("Cargando imagen"):
                    st.image(
                        info["Image URL"],
                        caption=selected_municipality,
                        use_column_width=True,
                    )

                indicators_json = API_KPI.get_inidicators(info["ID"])

                # st.json(indicators_json)
                st.markdown("### ¿Buscas más informacion del municipio?")
                st.subheader("2. Elige qué indicador quieres explorar")
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
                    show_indicator(years_data, selected_municipality, indicator.name)


def search_best_municipalities(indicators, k):
    data_municipalities = {}

    for i in indicators:
        municipalities = API_KPI.get_municipalities(i.id)

        # st.json(municipalities)

        for m in municipalities["municipalities"]:

            if m["id"] not in data_municipalities:
                data_municipalities[m["id"]] = {}

            last_year = max(m["years"][0].keys())
            last_value = m["years"][0][last_year]
            score = calculate_score(last_value)
            data_municipalities[m["id"]][i.id] = score * i.weight

    # st.json(data_municipalities)

    municipality_sums = []
    for municipality_id, indicators in data_municipalities.items():
        total_sum = sum(indicators.values())
        municipality_sums.append((municipality_id, total_sum))

    municipality_sums.sort(key=lambda x: x[1], reverse=True)
    top_k_municipalities = municipality_sums[:k]

    return top_k_municipalities


def find_municipality(df_municipios):

    indicators_json = API_KPI.get_all_indicators()

    # st.json(indicators_json)

    indicators = select_indicator_several(indicators_json)

    if indicators:
                    
        st.markdown("""
        #### 3. Asigna la escala de importancia

        1. **Menos importancia**: Este valor indica que el indicador no es relevante para ti.
        2. **Poca importancia**: El indicador es ligeramente importante, pero no decisivo.
        3. **Importancia moderada**: Consideras el indicador importante, pero no crucial.
        4. **Alta importancia**: El indicador es muy importante y debe ser tenido en cuenta.
        5. **Máxima importancia**: Este valor representa que el indicador es crítico para tu decisión.

        """)
        for i in indicators:
            value = st.slider(f"{i.name}", min_value=1, max_value=5, value=1, step=1)
            i.weight = value

        if st.button("Mostrar municipios recomendados para vivir"):

            with st.spinner("Buscando los mejores municipios..."):
                top_5_municipalities = search_best_municipalities(indicators, 5)

                filter_ids = [
                    municipality_id for municipality_id, _ in top_5_municipalities
                ]

                filtered_df = df_municipios[df_municipios["ID"].isin(filter_ids)]

                filtered_df["Puntuación"] = filtered_df["ID"].map(
                    dict(top_5_municipalities)
                )

                df_show = filtered_df[["Municipio", "Provincia", "Puntuación"]]

                df_show.set_index("Municipio", inplace=True)

                st.table(df_show.sort_values(by="Puntuación", ascending=False))

                filtered_municipios = search_coordinates(filtered_df)
                show_map_municipios(filtered_municipios)

                # filtered_municipios['Google Maps Enlace'] = filtered_municipios.apply(create_google_maps_link, axis=1)

                # st.table(filtered_municipios)


def create_google_maps_link(row):
    return f"https://www.google.com/maps/search/?api=1&query={row['Latitud']},{row['Longitud']}"


if __name__ == "__main__":

    logo = load_resources()

    df_municipios = load_municipios()

    st.sidebar.write(
        "<h1> Bizileku Bila </h1>  <h2><i>En busca de un lugar para vivir en Euskadi</i> </h2> ",
        unsafe_allow_html=True,
    )
    st.sidebar.write(logo, unsafe_allow_html=True)
    st.sidebar.markdown("[https://opendata.euskadi.eus](https://opendata.euskadi.eus)")

    st.sidebar.title("Navegación")
    selected_section = st.sidebar.radio(
        "Elige una sección:",
        [
            "Encuentra tu municipio ideal",
            "Explorar los municipios",
        ],
    )

    if selected_section == "Encuentra tu municipio ideal":
        st.title("Encuentra tu municipio ideal")

        st.markdown("### ¡Sigue estos 3 pasos para encontrar el municipio perfecto para ti!")

        st.subheader("1. Elige los grupos que te interesan ")


        find_municipality(df_municipios)

    elif selected_section == "Explorar los municipios":
        st.title("Explorar los municipios")

        st.markdown("**Selecciona un municipio del que quieras ver información**")

        st.subheader("¡Descubre lo que cada municipio te puede ofrecer!")
        search_municipality(df_municipios)
    else:
        pass
