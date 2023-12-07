import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import requests
import pprint

# Air Quality API
# based on Coordinates
def aqi_info(lat, lon):
    api_key = "e48892fb-d4f6-4cf4-bfc9-aa5ff9e98905"
    # lat = "1.3521"
    # lon = "103.8198"

    url = f"http://api.airvisual.com/v2/nearest_city?lat={lat}&lon={lon}&key={api_key}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    info = response.json()
    # pprint.pprint(info)

    aqi = info['data']['current']['pollution']['aqius']
    print(aqi)