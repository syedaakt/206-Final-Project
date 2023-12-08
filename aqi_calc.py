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
    print(city_id)
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

    print(aqi_avg_list)
    return aqi_avg_list
    # print(list(sum(north_east)/len(north_east), sum(north_west)/len(north_west), sum(south_east)/len(south_east), sum(south_west)/len(south_west)))

    # print(len(north_east))
    # print(len(north_west))
    # print(len(south_east))
    # print(len(south_west))

aqi_average()

def visualization_salary_data():

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
    
    # ax1.ticklabel_format(axis = 'x', style='plain')
    plt.title('AQI Levels of Hemispheres in the World')
    plt.xticks(rotation=45)
    plt.tight_layout()

# pie chart
    x2_axis = ['South America', 'Europe, Africa, Asia']
    y2_axis = []
    max = 0
    min = 5
    for avg in aqi_average():
        if avg > max:
            max = avg
    y2_axis.append(max)
    for avg in aqi_average():
        if avg < min:
            min = avg
    y2_axis.append(min)

  
    plt.subplot(1,2,2)
    plt.pie(y2_axis, labels=x2_axis, autopct='%1.1f%%')
    plt.title('AQI Level Based on Hemisphere Quadrant')

    plt.show()

# scatterplot
    plt.figure()

    cur.execute("SELECT jobs.job_title, employees.salary FROM employees JOIN jobs ON jobs.job_id = employees.job_id")

    res = cur.fetchall()

    x, y = zip(*res)

    # print()
    # print(x)
    # print()
    # print(y)

    # ('President', 'Administration Vice President', 'Administration Vice President', 'Administration Assistant', 'Administration Assistant', 'Administration Vice President', 'Administration Vice President', 'Public Accountant', 'Public Accountant', 'Accountant', 'Administration Assistant', 'Accountant')

    # (24000, 17000, 17000, 6000, 4800, 4800, 4200, 12000, 9000, 8200, 7700, 7800)

    plt.scatter(x,y)

    cur.execute("SELECT jobs.job_title, jobs.min_salary FROM jobs")

    res = cur.fetchall()

    x, y = zip(*res)

    plt.scatter(x, y, color='red', marker='x')

    cur.execute("SELECT jobs.job_title, jobs.max_salary FROM jobs")

    res = cur.fetchall()

    x, y = zip(*res)

    plt.scatter(x, y, color='red', marker='x')

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()
visualization_salary_data()