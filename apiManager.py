import json
import requests
import streamlit as st

'''

API Docs
 https://opendata.euskadi.eus/apis/-/apis-open-data/

'''

class APIManager():

    def __init__(self, base, headers=None):
        self.base = base
        self.headers = headers

    @st.cache_data
    def request(_self, route, keys):
        url = _self.base + route.format(**keys)
        response = requests.request("GET", url, headers=_self.headers)
        
        if response.status_code == 200:
            content = json.loads(response.text)
        else:
            content = "Error"
        
        return content


class APIMet(APIManager):

    def __init__(self, base, headers=None):
        super().__init__(base + "/euskalmet/", headers)

    def get_astro(self, day: int, month: int, year: int):
        return super().request(
            "astro/calendar/for/{YYYY}/{MM}/{DD}",
            {"YYYY": str(year), "MM": str(month), "DD": str(day)},
        )
    

class APIOcean(APIMet):
    def get_ocean_forecast(self, day: int, month: int, year: int, yyymmdd:str):
        """
        Get information like the text description for the full forecast in basque and spanish, and information like the water temperature and the visibility.
        """

        return super().request(
                "ocean/forecast/at/{YYYY}/{MM}/{DD}/for/{YYYYMMDD}",
                {"YYYY": str(year), "MM": str(month), "DD": str(day), "YYYYMMDD": yyymmdd},
            )
    


class APILocations(APIMet):

    regionsID = ["basque_country", "basque_cullinary"]

    def __init__(self, base, headers=None):
        super().__init__(base, headers)
        self.base = self.base + "geo/"

    def get_regions(self):
        return super().request(self.base + "regions", {})

    def get_zones(self, regionId):
        """
        Consult which locations in region and zone exist and specific data about them.
        """

        return super().request(
                "regions/{regionId}/zones",
                {"regionId": regionId},
            )
    


class APIkpi(APIManager):

    def __init__(self, base, headers=None):
        super().__init__(base + "/udalmap/", headers)


    def get_groups(self):
        return super().request("/groups", {})
    
    def get_inidicators(self, municipalityId):
        return super().request(
                        "indicators/municipalities/{municipalityId}",
                        {"municipalityId": municipalityId},
                    )

