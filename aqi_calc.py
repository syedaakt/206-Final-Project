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
    for aqi in res:
        cur.execute(
        """
        SELECT coordinates.id, coordinates.lat, airQualities.aqi
        FROM coordinates
        JOIN airQualities ON coordinates.id = airQualities.id
        WHERE airQualities.id = ?
        """
        , (aqi)
    )
        print(aqi)
    res = cur.fetchall()
    # print(res)

        # join where 
        # loop through citiies, join (info from multiple tables), where (check if the city corresponds with info), change coordinates into ids instead of ciites

cur, conn = setUpDatabase()
extract_aqi(cur, conn)