import streamlit as st
import requests
import pandas as pd
from os import listdir
from os.path import join

ENDPOINT = "https://api.euskadi.eus/sparql"
QUERIES_PATH = "./sparql/"


@st.cache_data
def load_queries():

    queries = {}

    ending = '.sparql'
    size = len(ending)  # Remove '.sparql' extension from the key

    for filename in listdir(QUERIES_PATH):

        if filename.endswith(ending):
            file_path = join(QUERIES_PATH, filename)
            with open(file_path, 'r') as file:

                queries[filename[:-size]] = file.read()

    return queries


@st.cache_data
def request(query: str = None) -> pd.DataFrame:

    headers = {
        "Accept": "application/sparql-results+json"
    }

    response = requests.get(ENDPOINT, params={'query': query}, headers=headers)

    try:

        if response.status_code == 200:
            data = response.json()
            bindings = data["results"]["bindings"]
        else:
            print(response.text)

    except Exception as e:
        print(e)
        print("Error")

    return bindings


@st.cache_data
def load_municipios():

    QUERIES = load_queries()

    location_q = QUERIES["prefix"] + QUERIES["locations"]

    #print(location_q)
    result = request(location_q)

    data_list = [
        {
            "Municipio": item["location_name"]["value"],
            "Provincia": item["provincia_name"]["value"],
            "ID": item["location"]["value"].split("/")[-1].replace("-", ""),
            "Qualifier": item["location_wikidata"]["value"].split("/")[-1],
        }
        for item in result
    ]

    return pd.DataFrame(data_list)


if __name__ == "__main__":

    print(load_municipios())
