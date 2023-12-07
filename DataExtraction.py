import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import pprint
      
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

#get terris list of capitals
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

#Create database
cur, conn = setUpDatabase('weather.db')

#Create cities table
cur.execute("CREATE TABLE IF NOT EXISTS cities (id INT PRIMARY KEY, city TEXT)")
conn.commit()
list_cities = get_cities() # returns a list of capital cities
cur.execute('SELECT COUNT(*) AS row_count FROM cities')
row_count = cur.fetchone()[0]
to_insert = list_cities[row_count:row_count + 25]
print(to_insert)
for i in range(len(to_insert)):
    cur.execute("INSERT OR IGNORE INTO cities (id, city) VALUES (?, ?)", (i, to_insert[i]))
conn.commit()


#Syeda's coordinates from terris capitals
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
print(city_coordinates)


#Create coordinates table
cur.execute("CREATE TABLE IF NOT EXISTS coordinates (city TEXT, lat NUMBER, lon NUMBER)")
conn.commit()
cur.execute('SELECT COUNT(*) AS row_count FROM coordinates')
row_count = cur.fetchone()[0]
to_insert = city_coordinates[row_count:row_count + 25]
for row in to_insert:
    cur.execute("INSERT OR IGNORE INTO coordinates (city, lat, lon) VALUES (?, ?, ?)", row)
conn.commit()

print(city_coordinates)
