import streamlit as st
from resourceManager import load_resources
from globals import api_ocean
from datetime import datetime, timedelta


def ocean():

    date_ini = st.date_input("Select the first date", datetime.now().date())
    date_end = st.date_input(
        "Select the second date", (datetime.now() + timedelta(days=1)).date()
    )

    data = api_ocean.get_ocean_forecast(
        date_ini.day, date_ini.month, date_ini.year, date_end.strftime("%Y%m%d")
    )

    # Optionally display the raw data
    st.header("Raw Data")
    st.json(data)

    st.title("Weather Forecast")

    st.header("General Information")
    st.write(f"Forecast Date: {data['for']}")
    st.write(f"Observation Time: {data['at']}")

    st.header("Forecast Description")
    st.subheader("In Spanish")
    st.write(data["forecastDescriptionByLang"]["SPANISH"])
    st.subheader("In Basque")
    st.write(data["forecastDescriptionByLang"]["BASQUE"])

    st.header("Forecast Text")
    st.subheader("In Spanish")
    st.write(data["forecastTextByLang"]["SPANISH"])
    st.subheader("In Basque")
    st.write(data["forecastTextByLang"]["BASQUE"])

    st.header("Conditions")
    st.write(
        f"Water Temperature: {data['waterTemperature']['value']} {data['waterTemperature']['unit']}"
    )
    st.write(f"Wave Height: {data['waveHeight']} meters")

    st.header("Visibility")
    st.write(f"Visibility: {data['visibility']['descriptionByLang']['SPANISH']}")


def main():

    logo = load_resources()

    st.sidebar.write("<h1> El tiempo en Euskadi </h1> ", unsafe_allow_html=True)
    st.sidebar.write(logo, unsafe_allow_html=True)

    ocean()


if __name__ == "__main__":
    main()
