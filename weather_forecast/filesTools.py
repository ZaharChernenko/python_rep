import os
import csv
from collections import namedtuple


def checkDirectory(path):
    try:
        os.makedirs(path)

    except FileExistsError:
        print("Directory already exists")


def loadUserData() -> str:
    """Returns string"""
    with open("./data/user_data.json", "r", encoding="utf-8") as fin:
        file_check = fin.read().strip()
        return file_check


CityTuple = namedtuple("CityTuple", "name lat lon")


def readCityDict() -> dict:
    with open("./data/city_list.csv", "r", encoding="UTF-8") as fin:
        csv_reader = csv.reader(fin)
        next(csv_reader)
        cities_dict = {}
        for line in csv_reader:
            cities_dict.setdefault(line[1], [])
            cities_dict[line[1]].append(CityTuple(line[0], line[4], line[5]))
        return cities_dict
