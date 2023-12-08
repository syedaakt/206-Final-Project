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
#print(to_insert)
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
#print(city_coordinates)


#Create coordinates table
cur.execute("CREATE TABLE IF NOT EXISTS coordinates (city TEXT, lat NUMBER, lon NUMBER)")
conn.commit()
cur.execute('SELECT COUNT(*) AS row_count FROM coordinates')
row_count = cur.fetchone()[0]
to_insert = city_coordinates[row_count:row_count + 25]
for row in to_insert:
    cur.execute("INSERT OR IGNORE INTO coordinates (city, lat, lon) VALUES (?, ?, ?)", row)
conn.commit()

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

extract_latandlon()

# joys air quality data
# def aqi_info():
#     # lat = "1.3521"
#     # lon = "103.8198"
#     # count = 0
#     for coortup in extract_latandlon()[:10]:
#         api_key = "076da2eb-8d89-4c54-8b3d-9e32d4b01b1f"
#         lat = str(coortup[0])
#         lon = str(coortup[1])
#         # print(lat, lon)
#         url = f"http://api.airvisual.com/v2/nearest_city?lat={lat}&lon={lon}&key={api_key}"
#         payload={}
#         headers = {}
#         response = requests.request("GET", url, headers=headers, data=payload)
#         # if response.status_code==200:
#         info = response.json()
#         aqi = info['data']['current']['pollution']['aqius']
#         print(aqi)
#             # return aqi
#         # else:
#             # print('!!!!!!!!!!!!!!!!!!!!!!! NOPE')
#         # count+=1
#     # print(count)

# aqi_info()

def aqi_info():
    # lat = "1.3521"
    # lon = "103.8198"
    # count = 0
    for coortup in extract_latandlon()[6:12]:
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
            print(data)
        else:
            print(f"Error: {response.status_code} - {response.text}")
        # headers = {
        # 'Content-Type': 'application/json',
        # 'Api-Key': api_key
        # }
        # response = requests.get(url, headers=headers)
        # if response.status_code==200:
        #     data = response.json()
        #     if 'results' in data and data['results']:
        #         result = data['results'][0]
        #         print(f"Location: {result['location']}")
        #         print(f"Timestamp: {result['date']['utc']}")
        #         print(f"PM2.5 Concentration: {result['value']} {result['unit']}")
        #     else:
        #         print("No air quality data found for the specified location")
        # else:
        #     print(f"Error: {response.status_code} - {response.text}")



        # payload={}
        # headers = {}
        # response = requests.request("GET", url, headers=headers, data=payload)
        # # if response.status_code==200:
        # info = response.json()
        # aqi = info['data']['current']['pollution']['aqius']
        # print(aqi)
            # return aqi
        # else:
            # print('!!!!!!!!!!!!!!!!!!!!!!! NOPE')
        # count+=1
    # print(count)

aqi_info()



# air_qualities = []
# for cords in city_coordinates:
#     air_qualities.append((cords[0],aqi_info(str(cords[1]), str(cords[2]))))
#     # print(air_qualities)

    


# cur.execute("CREATE TABLE IF NOT EXISTS airQualities (city TEXT, airQuality NUMBER)")
# conn.commit()
# cur.execute('SELECT COUNT(*) AS row_count FROM airQualities')
# row_count = cur.fetchone()[0]
# to_insert = air_qualities[row_count:row_count + 25]
# for row in to_insert:
#     cur.execute("INSERT OR IGNORE INTO airQualities (city, airQuality) VALUES (?, ?)", row)
# conn.commit()

# print(city_coordinates)
