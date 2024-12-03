import csv
import json


def getCityList(city_dict: dict) -> list:
    return list(city_dict.values())

def readCititesList() -> list:
    with open("./city_list.json", encoding="utf-8") as fin:
        cities_list = json.load(fin, object_hook=getCityList)
        for city in cities_list:
            city.extend(reversed(city.pop()))
        cities_list.sort(key=lambda elem: elem[0])
        return cities_list


def writeCitiesList(cities_list: list) -> None:
    with open("./city_list.csv", "w", encoding="UTF-8") as fout:
        writer = csv.writer(fout, delimiter=',')
        writer.writerow(["name", "country", "id", "code", "lat", "lon"])
        for city in cities_list:
            writer.writerow(city)

writeCitiesList(readCititesList())
print("Done!")

