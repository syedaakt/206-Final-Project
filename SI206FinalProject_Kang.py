from bs4 import BeautifulSoup
import re
import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt

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
                cities_list.append(countries_list[each])
        print(sorted(cities_list))
        return sorted(cities_list)

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

cur, conn = setUpDatabase('capital cities')


cur.execute("CREATE TABLE IF NOT EXISTS cities (id NUMBER, city TEXT)")
conn.commit()

# cities = get_cities() # returns a list of capital cities

cur.execute('SELECT COUNT(*) AS row_count FROM cities')
row_count = cur.fetchone()[0]

to_insert = cities[row_count:row_count + 1]
for row in to_insert:
    cur.execute("INSERT OR IGNORE INTO cities (id, city) VALUES (?, ?)", row)

conn.commit()
        


class TestCases(unittest.TestCase):
    def test_get_cities(self):
        self.test = get_cities()
        self.assertNotIn('United States of America', self.test)
        self.assertNotIn('China', self.test)
        self.assertIn('Beijing', self.test)

def main():
    get_cities()

if __name__ == '__main__':
    unittest.main(verbosity=2)