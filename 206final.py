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

cur, conn = setUpDatabase('weather.db')
cur.execute("CREATE TABLE IF NOT EXISTS coordinates (city TEXT, lat NUMBER, lon NUMBER)")
conn.commit()



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
# get_cities()

# cities = ['London','Abu Dhabi','Abuja', 'Accra', 'Addis Ababa', 'Algiers', 'Amman', 'Amsterdam', 'Andorra la Vella', 'Ankara', 'Antananarivo', 'Apia', 'Ashgabat', 'Asmara', 'Astana', 'Asunción', 'Athens', 'Baghdad', 'Baku', 'Bamako', 'Bandar Seri Begawan', 'Bangkok', 'Bangui', 'Banjul', 'Basseterre', 'Beijing', 'Beirut', 'Belgrade', 'Belmopan', 'Berlin', 'Bern', 'Bishkek', 'Bissau', 'Bogotá', 'Brasilia', 'Bratislava', 'Brazzaville', 'Bridgetown', 'Brussels', 'Bucharest', 'Budapest', 'Buenos Aires', 'Cairo', 'Canberra', 'Caracas', 'Castries', 'Chisinau', 'Conakry', 'Copenhagen', 'Dakar', 'Damascus', 'Dhaka', 'Dili', 'Djibouti (city)', 'Dodoma', 'Doha', 'Dublin', 'Dushanbe', 'Freetown', 'Funafuti', 'Gaborone', 'Georgetown', 'Gitega', 'Guatemala City', 'Hanoi', 'Harare', 'Havana', 'Helsinki', 'Honiara', 'Islamabad', 'Jakarta', 'Jerusalem', 'Jerusalem (East)', 'Juba', 'Kabul', 'Kampala', 'Kathmandu', 'Khartoum', 'Kigali', 'Kingston', 'Kingstown', 'Kinshasa', 'Kuala Lumpur', 'Kuwait City', 'Kyiv (also known as Kiev)', 'Libreville', 'Lilongwe', 'Lima', 'Lisbon', 'Ljubljana', 'Lomé', 'London', 'Luanda', 'Lusaka', 'Luxembourg (city)', 'Madrid', 'Majuro', 'Malabo (de jure), Oyala (seat of government)', 'Male', 'Managua', 'Manama', 'Manila', 'Maputo', 'Maseru', 'Mbabane (administrative), Lobamba (legislative, royal)', 'Mexico City', 'Minsk', 'Mogadishu', 'Monaco', 'Monrovia', 'Montevideo', 'Moroni', 'Moscow', 'Muscat', "N'Djamena", 'Nairobi', 'Nassau', 'Naypyidaw', 'New Delhi', 'Ngerulmud', 'Niamey', 'Nicosia', 'Nouakchott', 'Nukuʻalofa', 'Oslo', 'Ottawa', 'Ouagadougou', 'Palikir', 'Panama City', 'Paramaribo', 'Paris', 'Phnom Penh', 'Podgorica', 'Port Louis', 'Port Moresby', 'Port Vila', 'Port of Spain', 'Port-au-Prince', 'Porto-Novo', 'Prague', 'Praia', 'Pretoria (administrative), Cape Town (legislative), Bloemfontein (judicial)', 'Pristina', 'Pyongyang', 'Quito', 'Rabat', 'Reykjavik', 'Riga', 'Riyadh', 'Rome', 'Roseau', "Saint George's", "Saint John's", 'San Jose', 'San Marino', 'San Salvador', "Sana'a", 'Santiago', 'Santo Domingo', 'Sarajevo', 'Seoul', 'Singapore', 'Skopje', 'Sofia', 'Sri Jayawardenepura Kotte', 'Stockholm', 'Sucre (de jure), La Paz (seat of government)', 'Suva', 'São Tomé', 'Taipei', 'Tallinn', 'Tarawa', 'Tashkent', 'Tbilisi', 'Tegucigalpa', 'Tehran', 'Thimphu', 'Tirana', 'Tokyo', 'Tripoli', 'Tunis', 'Ulaanbaatar', 'Vaduz', 'Valletta', 'Vatican City', 'Victoria', 'Vienna', 'Vientiane', 'Vilnius', 'Warsaw', 'Washington, D.C.', 'Wellington', 'Windhoek', 'Yamoussoukro', 'Yaounde', 'Yaren District (de facto)', 'Yerevan', 'Zagreb']
# print(cities)
cities= get_cities()
city_coordinates = [] 
API_KEY = '466d3d6a8030052dd52e9a49585f562a'
for city in cities: 
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}'
    
    r = requests.get(url)
    if r.status_code==200:
        # pprint.pprint(r.json()[0])
        r = r.json()[0]
        # print(r)
    # else:
    #     print('DIDNT WORK')
    city_coordinates.append((city, r['lat'], r['lon']))
print(city_coordinates)

cur.execute('SELECT COUNT(*) AS row_count FROM coordinates')
row_count = cur.fetchone()[0]

to_insert = city_coordinates[row_count:row_count + 25]
for row in to_insert:
    cur.execute("INSERT OR IGNORE INTO coordinates (city, lat, lon) VALUES (?, ?, ?)", row)

conn.commit()
print(city_coordinates)
# for t in city_coordinates:
#     url = f'https://history.openweathermap.org/data/2.5/history/city?lat={t[1]}&lon={t[2]}&appid="6034a57af0a951949dd91ac6907654cd"'
#     r = requests.get(url).json()
#     print(r)