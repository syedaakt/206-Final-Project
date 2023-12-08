import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import pprint

# Set up database  
def setUpDatabase():
    weatherdb = 'weather.db'
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+weatherdb)
    cur = conn.cursor()
    return cur, conn

# Get AQI from database
def extract_aqi(cur, conn):
    cur.execute(

    """

    SELECT id 
    FROM coordinates
    """
    )
    res = cur.fetchall()
    # print(res)
    all_info = []
    for aqi in res:
        cur.execute(
        """
        SELECT coordinates.id, coordinates.lat, coordinates.lon, airQualities.aqi
        FROM coordinates
        JOIN airQualities ON coordinates.id = airQualities.id
        WHERE airQualities.id = ?
        """
        , (aqi)
    )
        # print(aqi)
        res = cur.fetchall()
        all_info.append(res[0])
    # print(all_info)
    return all_info

cur, conn = setUpDatabase()
extract_aqi(cur, conn)

# # Get the city and it's corresponding ID
# def extract_cityID(curr, conn):
#     cur.execute(
#         """
#         SELECT cities.city, airQualities.aqi
#         FROM cities
#         JOIN airQualities ON cities.id = airQualities.id
#         WHERE airQualities.id = ?
#         """
#         , 
#     )
#     city_id = cur.fetchall()
#     print(city_id)
#     return city_id

# cur, conn = setUpDatabase()
# extract_cityID(cur, conn)

# Calculate the average AQI based on the city's hemisphere
def aqi_average():
    north_east = []
    north_west = []
    south_east = []
    south_west = []
    for info in extract_aqi(cur, conn):
        id = info[0]
        lat = info[1]
        lon = info[2]
        aqi = info[3]
        if lat > 0:
            if lon > 0:
                north_east.append(aqi)
            else:
                north_west.append(aqi)
        else:
            if lon > 0:
                south_east.append(aqi)
            else:
                south_west.append(aqi)
    
    aqi_avg_list = []
    aqi_avg_list.append(sum(north_east)/len(north_east))
    aqi_avg_list.append(sum(north_west)/len(north_west))
    aqi_avg_list.append(sum(south_east)/len(south_east))
    aqi_avg_list.append(sum(south_west)/len(south_west))

    print(aqi_avg_list)
    return aqi_avg_list
    # print(list(sum(north_east)/len(north_east), sum(north_west)/len(north_west), sum(south_east)/len(south_east), sum(south_west)/len(south_west)))

    # print(len(north_east))
    # print(len(north_west))
    # print(len(south_east))
    # print(len(south_west))

aqi_average()
