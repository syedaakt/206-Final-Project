import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import pprint

# def get_cities():
#     source_dir = os.path.dirname(__file__)
#     fullpath = os.path.join(source_dir, f'SI206--FinalProject--CapitalCities2.html')
#     with open(fullpath, 'r', encoding="utf-8-sig") as htmlfile:
#         rawsoup = htmlfile.read()
#         soup = BeautifulSoup(rawsoup, 'html.parser')
#         countries = soup.find_all('td')
#         countries_list = []
#         for coun in countries:
#             if len(coun.text)!=1:
#                 countries_list.append(coun.text)
#         cities_list = []
#         for each in range(len(countries_list)):
#             if each%2!=0:
#                 cities_list.append(countries_list[each])
#         print(sorted(cities_list))
#         return sorted(cities_list)
        
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

cur, conn = setUpDatabase('weather')

cur.execute("CREATE TABLE IF NOT EXISTS coordinates (city TEXT, lat NUMBER, lon NUMBER)")
conn.commit()

API_KEY = '466d3d6a8030052dd52e9a49585f562a'

#get terris list of capitals
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
            cities_list.append(countries_list[each])

cities = sorted(cities_list)

city_coordinates = [] 

for city in cities: 
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}'
    
    r = requests.get(url).json()[0]

    city_coordinates.append((city, r['lat'], r['lon']))

cur.execute('SELECT COUNT(*) AS row_count FROM coordinates')
row_count = cur.fetchone()[0]

to_insert = city_coordinates[row_count:row_count + 1]
for row in to_insert:
    cur.execute("INSERT OR IGNORE INTO coordinates (city, lat, lon) VALUES (?, ?, ?)", row)

conn.commit()
print(city_coordinates)
# for t in city_coordinates:
#     url = f'https://history.openweathermap.org/data/2.5/history/city?lat={t[1]}&lon={t[2]}&appid="6034a57af0a951949dd91ac6907654cd"'
#     r = requests.get(url).json()
#     print(r)