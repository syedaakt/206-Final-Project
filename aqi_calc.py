import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import pprint
import numpy as np
import csv


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
        res = cur.fetchall()
        all_info.append(res[0])
    return all_info

cur, conn = setUpDatabase()
extract_aqi(cur, conn)

# Get the city and it's corresponding ID
def extract_cityID(curr, conn):
    cur.execute(
        """
        SELECT id
        FROM cities
        """
    )
    res = cur.fetchall()
    city_id = []
    for id in res:
        cur.execute(
            """
            SELECT cities.id, cities.city, airQualities.aqi
            FROM cities
            JOIN airQualities ON cities.id = airQualities.id
            WHERE airQualities.id = ?
            """
            , (id)
        )
        res = cur.fetchall()
        city_id.append(res[0])
    return city_id

cur, conn = setUpDatabase()
extract_cityID(cur, conn)

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

    return aqi_avg_list

def create_barandpie():

# horizontal bar chart
    x_axis = ['north_east', 'north_west', 'south_east', 'south_west']
    y_axis = []
    for avg in aqi_average():
        y_axis.append(avg)

    plt.figure(figsize = (10,5))
    plt.subplot (1, 2, 1)
    plt.bar(x_axis, y_axis)
    plt.xlabel('Hemisphere')
    plt.ylabel('Average AQI')
    
    plt.title('AQI Levels of Hemispheres in the World')
    plt.xticks(rotation=45)
    plt.tight_layout()

# pie chart
    lvl_1 = 0
    lvl_2 = 0
    lvl_3 = 0
    lvl_4 = 0
    lvl_5 = 0

    for info in extract_aqi(cur, conn):
        if info[3] == 1:
            lvl_1 += 1
        if info[3] == 2:
            lvl_2 += 1
        if info[3] == 3:
            lvl_3 += 1
        if info[3] == 4:
            lvl_4 += 1
        if info[3] == 5:
            lvl_5 += 1

    list_lvl = [lvl_1, lvl_2, lvl_3, lvl_4, lvl_5]
    list_labels = ["AQI: 1", "AQI: 2", "AQI: 3", "AQI: 4", "AQI: 5"]
    plt.subplot(1,2,2)
    plt.pie(list_lvl, labels=list_labels, autopct='%1.2f%%')
    plt.title('Percentage of Cities in Each AQI Level')

    plt.show()

# scatterplot
def create_scatterplot():
    plt.figure(figsize=(10,8))
    city_list = []
    cities = extract_cityID(cur, conn)
    for tup in cities:
        id2 = tup[0]
        city = tup[1]
        aqi2 = tup[2]

        south_west = []
    
        for info in extract_aqi(cur, conn):
            id = info[0]
            lat = info[1]
            lon = info[2]
            aqi = info[3]
            if lat < 0:
                if lon < 0:
                    south_west.append(id)
        for the_id in south_west:
            if the_id == id2:
                city_list.append((city, aqi2))

    for plot in city_list:
        the_city = plot[0]
        the_aqi = plot[1]
        
        plt.subplot()
        plt.scatter(the_city, the_aqi, color='olive')
        plt.xticks(rotation=45)
        plt.title('AQI Levels of Cities in Lowest AQI Average Hemisphere (South-West Hemisphere)')

    plt.show()

# Create calculation CSV file
def create_csv():
    source_dir = os.path.dirname(__file__)
    fullpath = os.path.join(source_dir, 'AQI_Calculation.csv')
    header = ['Northeast Average AQI', 'Northwest Average AQI', 'Southeast Average AQI', 'Southwest Average AQI']
    data = aqi_average()
    # for avg in aqi_average():
    #     data.append([avg])
    # print(data)
    with open(fullpath, 'w', encoding="utf-8-sig", newline = "") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        csvwriter.writerow(data)

def main():
    aqi_average()
    create_barandpie()
    create_scatterplot()
    create_csv()

if __name__ == '__main__':
    main()
