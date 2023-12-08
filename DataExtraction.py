import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import pprint

#set up database      
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# get terris list of capitals
def get_cities():
    source_dir = os.path.dirname(__file__)
    fullpath = os.path.join(source_dir, f'SI206--FinalProject--CapitalCities2.html')
    with open(fullpath, 'r', encoding="utf-8-sig") as htmlfile:
        rawsoup = htmlfile.read()
        soup = BeautifulSoup(rawsoup, 'html.parser')
        countries = soup.find_all('td')
        countries_list = []
        for coun in countries:
            if len(coun.text)!=1:
                countries_list.append(coun.text)
        cities_list = []
        for each in range(len(countries_list)):
            if each%2!=0:
                each = countries_list[each].split()
                cities_list.append(each[0])
        # print(sorted(cities_list))
    return sorted(cities_list)

# Syeda's coordinates from terris capitals
def get_coordinates():
    city_coordinates = [] 
    API_KEY = '466d3d6a8030052dd52e9a49585f562a'
    for city in list_cities: 
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}'
        
        r = requests.get(url)
        if r.status_code==200:
            r = r.json()[0]
        else:
            print('DIDNT WORK')
        city_coordinates.append((city, r['lat'], r['lon']))
    return city_coordinates

# joys air quality data
def aqi_info():
    # lat = "1.3521"
    # lon = "103.8198"
    # count = 0
    air_qualities = []
    for coortup in extract_latandlon():
        api_key = "442aabd8dfc8f8918479da933cc4e5ef"
        lat = coortup[0]
        lon = coortup[1]
        # coordinates = lat + ',' + lon
        # print(lat, lon)
        url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
        endpoint = url.format(lat, lon, api_key)
        response = requests.get(endpoint)
        if response.status_code==200:
            data = response.json()
            aqi = data['list'][0]['main']['aqi']
            air_qualities.append(aqi)
            # print(aqi)
        else:
            print(f"Error: {response.status_code} - {response.text}")
    # print(len(air_qualities))
    return air_qualities

# Get the latitude and longitude data
def extract_latandlon():
    cur.execute(
        """
        SELECT coordinates.lat, coordinates.lon
        FROM coordinates
        """
    )
    res = cur.fetchall()
    conn.commit
    return res
    # print(res)


# Create database name
cur, conn = setUpDatabase('weather.db')
#lala
#Create cities table
cur.execute("CREATE TABLE IF NOT EXISTS cities (id INT PRIMARY KEY, city TEXT)")
conn.commit()
list_cities = get_cities() # returns a list of capital cities
cur.execute('SELECT COUNT(*) AS row_count FROM cities')
row_count = cur.fetchone()[0]
to_insert = list_cities[row_count:row_count + 25]
#print(to_insert)
for i in range(len(to_insert)):
    cur.execute("INSERT OR IGNORE INTO cities (id, city) VALUES (?, ?)", (i, to_insert[i]))
conn.commit()

# Create coordinates table
cur.execute("CREATE TABLE IF NOT EXISTS coordinates (city TEXT, lat NUMBER, lon NUMBER)")
conn.commit()
cur.execute('SELECT COUNT(*) AS row_count FROM coordinates')
city_coordinates= get_coordinates()
row_count = cur.fetchone()[0]
to_insert = city_coordinates[row_count:row_count + 25]
for row in to_insert:
    cur.execute("INSERT OR IGNORE INTO coordinates (city, lat, lon) VALUES (?, ?, ?)", row)
conn.commit()

#extract_latandlon()
#print(len(aqi_info()))

#create table for air qualities
cur.execute("CREATE TABLE IF NOT EXISTS airQualities (id INT PRIMARY KEY, aqi NUMBER)")
conn.commit()
list_aqis = aqi_info()
cur.execute('SELECT COUNT(*) AS row_count FROM airQualities')
row_count = cur.fetchone()[0]
to_insert = list_aqis[row_count:row_count + 25]
for row in range(len(to_insert)):
    cur.execute("INSERT OR IGNORE INTO airQualities (id, aqi) VALUES (?, ?)",(row, to_insert[row]))
conn.commit()
