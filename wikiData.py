import streamlit as st
from wikidata.client import Client

CLIENT = Client()


@st.cache_data
def get_entity_data(qualifier):
    img_url = None
    latitude = None
    longitude = None

    entity = CLIENT.get(qualifier, load=True)

    description = entity.description.get("es", None)

    image_prop = CLIENT.get("P18")
    image = entity.get(image_prop, None)
    if image:
        img_url = image.image_url

    coordinates_prop = CLIENT.get("P625")
    coordinates = entity.get(coordinates_prop, None)
    if coordinates:
        latitude = coordinates.latitude
        longitude = coordinates.longitude

    
    sitelinks = entity.data.get("sitelinks", {})
    spanish_wikipedia = sitelinks.get('eswiki', {}).get('url', None)

    return {
        "description": description,
        "img_url": img_url,
        "latitude": latitude,
        "longitude": longitude,
        "wiki_url": spanish_wikipedia
    }


if __name__ == "__main__":

    print(get_entity_data("Q1242411"))
