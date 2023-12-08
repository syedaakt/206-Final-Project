import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import requests
import pprint
from bs4 import BeautifulSoup

# Air Quality API
# based on Coordinates
def aqi_info(lat, lon):
    api_key = "076da2eb-8d89-4c54-8b3d-9e32d4b01b1f"
    # lat = "1.3521"
    # lon = "103.8198"

    url = f"http://api.airvisual.com/v2/nearest_city?lat={lat}&lon={lon}&key={api_key}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    info = response.json()
    # print(info)
    # pprint.pprint(info)

    aqi = info['data']['current']['pollution']['aqius']
    print(aqi)
aqi_info("-25.966213", "32.56745")




# def aqi_info(lat, lon):
#     api_key = "7fd8f916-c802-420b-8287-9e9c5ea3a989"
#     # lat = "1.3521"
#     # lon = "103.8198"
#     url = f"http://api.airvisual.com/v2/nearest_city?lat={lat}&lon={lon}&key={api_key}"
#     payload={}
#     headers = {}
#     r = requests.get(url)
#     # if r.status_code==200:
#     #     r = r.json()[0]
#     # else:
#     #     print('DIDNT WORK')
#     response = requests.request("GET", url, headers=headers, data=payload)
#     info = response.json()
#     print(info)

#     #with open('aqui.json', 'w') as aqi_file:
#         #json.dump(info, aqi_file)
#     # if response.status_code==200:
#     #     info = response.json()
#     #     aqi = info['data']['current']['pollution']['aqius']
#     #     print(aqi)
#     # else:
#     #     print('!!!!!!!!!!!!!!!!!!!!!!!!!!! NOPE')
# aqi_info("36.7753606", "3.0601882")