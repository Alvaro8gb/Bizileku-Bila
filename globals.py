import os
import dotenv

from apiManager import *

"""
JSON Web Token
Is an open standard (RFC-7519) based on
JSON consisting of a token that is used to send data
between applications or services and ensure that it is valid and secure.

"""

dotenv.load_dotenv()

JWT = os.getenv("JWT")
BASE_URL = "https://api.euskadi.eus/"


headers = {
    "Authorization": "Bearer" + " " + JWT,
}

API_MET = APIMet(BASE_URL, headers)
API_OCEAN = APIOcean(BASE_URL)
API_LOCATIONS = APILocations(BASE_URL)
API_KPI = APIkpi(BASE_URL)


if __name__ == "__main__":

    # zones = api_locations.get_zones("basque_country")

    # for z in zones:
    #  print(z["regionZoneId"])

    # print(api_met.get_regions())
    # print(api_met.get_astro(2, 11, 2022))

    #print(API_KPI.get_groups())
    
    
    for e in API_KPI.get_inidicators("48001")["indicators"]:
        print(e, "\n\n")
    
    indicators = API_KPI.get_all_indicators()

    for i in indicators:
        print(i)

    print(len(indicators))
