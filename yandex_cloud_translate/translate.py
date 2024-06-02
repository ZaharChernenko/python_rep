import re
import json
import gettext
import pycountry
from googletrans import Translator
from functools import lru_cache
import requests

IAM_TOKEN = ('t1.9euelZqSzImPjpWcyMyPkpyJksmNyO3rnpWax5jPkc3LiZ6bkcyNyYyKkonl8_cZTwdZ-e9RcXdF_t3z91l9BFn571Fxd0X'
             '-zef1656VmsnNnZvImM3Ji8yNlZ2NjYqM7_zF656VmsnNnZvImM3Ji8yNlZ2NjYqM'
             '.bPR8oJI6ScB27d53UfI360_xSE_KDASFVKa5vdyvvNK6jixnnzjLCxf49XpMGjfK1KLMRlm2gZWBYUx9hfnfBQ')
folder_id = 'b1guulndhvhq8gmgo6cg'
target_language = 'ru'
texts = ["Hello", "World"]

body = {
    "targetLanguageCode": target_language,
    "texts": texts,
    "folderId": folder_id,
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer {0}".format(IAM_TOKEN)
}


@lru_cache(256)
def translate2Russian(word):
    body["texts"] = word
    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                             json=body,
                             headers=headers
                             )
    return response.json()["translations"][0]["text"]


translator = Translator()
ru_countries = gettext.translation('iso3166', pycountry.LOCALES_DIR, languages=['ru'])
ru_countries.install()


@lru_cache(256)
def code2CountryName(code):
    """Получает на вход двухсимвольный код страны, расшифровывает его
    на английский, а потом переводит на русский c помощью gettext, если не получилось,
    то с googletrans"""
    country_data = pycountry.countries.get(alpha_2=code)
    if not country_data:
        return "Косово" if code == "XK" else code
    country_data = _(country_data.name.split(",")[0])
    if re.match("[A-z]", country_data):
        country_data = translator.translate(country_data, dest="ru", src="en").text
    return country_data


def readValues(dictionary):
    if "name" in dictionary:
        if not dictionary["country"]:
            return None
        return {"name": dictionary["name"], "country": dictionary["country"], "id": dictionary["id"]}
    return None


with open("city.list.json", "r") as fin:
    list_of_dicts = json.load(fin, object_hook=readValues)


def createTranslatedFile():
    try:
        for city in list_of_dicts:
            if city is None:
                list_of_dicts.remove(city)
                continue

            elif len(city) == 4:
                continue

            elif city["country"] in ("BY", "RU", "UA"):
                city["name"] = translate2Russian(city["name"])
                if re.match("[A-z]", city["name"]):
                    list_of_dicts.remove(city)

            city["code"] = city["country"]
            city["country"] = code2CountryName(city["code"])

    except Exception:
        print("Exception")
        with open("translated.json", "w") as fout:
            json.dump(list_of_dicts, fout, indent="\t", ensure_ascii=False)
        createTranslatedFile()


createTranslatedFile()
print(code2CountryName.cache_info())
print(translate2Russian.cache_info())

with open("translated.json", "w") as fout:
    json.dump(list_of_dicts, fout, indent="\t", ensure_ascii=False)
