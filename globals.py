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

MET = APIMet(BASE_URL, headers)
OCEAN = APIOcean(BASE_URL, headers )
LOCATIONS = APILocations(BASE_URL, headers)
KPI = APIkpi(BASE_URL, headers)



if __name__ == "__main__":
    
  #zones = api_locations.get_zones("basque_country")

  #for z in zones: 
    #  print(z["regionZoneId"])

  # print(api_met.get_regions())
  #print(api_met.get_astro(2, 11, 2022))


  
  print(KPI.get_groups())
  KPI.get_inidicators("48001")