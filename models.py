import html
from typing import List, Dict, Optional
from pydantic import BaseModel


class Indicator(BaseModel):
    id: str
    name: str
    group: str
    subgroup: str
    weight: Optional[int] = 0
    years: Optional[Dict[str, float]] = None  # Make 'years' optional


def parse_indicator(json_data: dict):
    years = json_data.get("years", [None])[0] if json_data.get("years") else None

    return Indicator(
        id=json_data["id"],
        name=html.unescape(json_data["name"]),
        group=json_data["_links"]["group"]["name"],
        subgroup=json_data["_links"]["subgroup"]["name"],
        years=years,
    )


def create_indicators(indicators_json: dict):
    return {
        html.unescape(indicator["name"]): parse_indicator(indicator) for indicator in indicators_json
    }


if __name__ == "__main__":

    json_data_municipality = {
        "id": "140",
        "name": "Contenedores para la recogida de ropa/textiles ( &#x2030; habitantes)",
        "years": [{"2005": 0.0, "2006": 0.0, "2007": 0.0, "2008": 0.0, "2009": 0.0}],
        "_links": {
            "self": {
                "name": "Contenedores para la recogida de ropa/textiles ( &#x2030; habitantes)",
                "href": "https://api.euskadi.eus/udalmap/indicators/140",
            },
            "subgroup": {
                "name": "Residuos",
                "href": "https://api.euskadi.eus/udalmap/subgroups/M.1",
            },
            "group": {
                "name": "Medioambiente y Movilidad",
                "href": "https://api.euskadi.eus/udalmap/groups/M",
            },
        },
    }

    json_data_indicators = {
        "id": "132",
        "name": "Teléfonos públicos (por cada 1.500 habitantes)",
        "_links": {
            "self": {
                "name": "Teléfonos públicos (por cada 1.500 habitantes)",
                "href": "https://api.euskadi.eus/udalmap/indicators/132",
            },
            "subgroup": {
                "name": "Equipamientos de uso colectivo",
                "href": "https://api.euskadi.eus/udalmap/subgroups/S.7",
            },
            "group": {
                "name": "Cohesión social / Calidad de vida",
                "href": "https://api.euskadi.eus/udalmap/groups/S",
            },
        },
    }

    print(parse_indicator(json_data_municipality))
    print(parse_indicator(json_data_indicators))
