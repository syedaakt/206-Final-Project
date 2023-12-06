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