import asyncio
import json
import time

import aiohttp
import requests
from bs4 import BeautifulSoup  # pip install bs4


def getData(url: str):
    try:
        return requests.get(url, timeout=4)
    except requests.exceptions.ReadTimeout:
        return getData(url)


async def asyncParser(session: aiohttp.client.ClientSession, page: int):
    cur_page_url: str = URL_PATH + str(page)
    async with session.get(url=cur_page_url) as responce:
        responce_text = await responce.text()

        soup = BeautifulSoup(responce_text, "html.parser")
        name = soup.findAll("td", {"class": "views-field-title"})
        calories = soup.findAll("td", {"class": "views-field views-field-field-kcal-value"})
        protein = soup.findAll("td", {"class": "views-field views-field-field-protein-value"})
        fat = soup.findAll("td", {"class": "views-field views-field-field-fat-value"})
        carb = soup.findAll("td", {"class": "views-field views-field-field-carbohydrate-value"})

        for i in range(len(name)):
            async_database.append({
                "name": name[i].text[1:-1],
                "calories": calories[i].text[1:-1],
                "protein": protein[i].text[1:-1],
                "fat": fat[i].text[1:-1],
                "carb": carb[i].text[1:-1]
            })

        print(f"Получена страница {page}")


async def gatherData(last_page: int):
    async with aiohttp.ClientSession() as session:  # асинхронный контекстный менеджер
        tasks: list[asyncio.Task] = []
        for page in range(last_page):
            # создаем конкурентные задачи из корутин
            tasks.append(asyncio.create_task(asyncParser(session, page)))
        await asyncio.gather(*tasks)


def parser(url_path: str, last_page: int):
    for page in range(last_page):
        print(page)
        cur_page_url: str = url_path + str(page)
        soup = BeautifulSoup(getData(cur_page_url).text, "html.parser")
        name = soup.findAll("td", {"class": "views-field-title"})
        calories = soup.findAll("td", {"class": "views-field views-field-field-kcal-value"})
        protein = soup.findAll("td", {"class": "views-field views-field-field-protein-value"})
        fat = soup.findAll("td", {"class": "views-field views-field-field-fat-value"})
        carb = soup.findAll("td", {"class": "views-field views-field-field-carbohydrate-value"})

        for i in range(len(name)):
            database.append({
                "name": name[i].text[1:-1],
                "calories": calories[i].text[1:-1],
                "protein": protein[i].text[1:-1],
                "fat": fat[i].text[1:-1],
                "carb": carb[i].text[1:-1]
            })


URL_PATH: str = "https://calorizator.ru/product/all?page="
database: list[dict] = []
async_database: list[dict] = []
html: BeautifulSoup = BeautifulSoup(getData(URL_PATH).text, "html.parser")
LAST_PAGE: int = int(html.find("li", {"class": "pager-last"}).text)


# start: float = time.time()
# parser(URL_PATH, LAST_PAGE)
# print(f"Время исполнения синхронного парсера: {time.time() - start}")


start = time.time()
asyncio.run(gatherData(LAST_PAGE))  # запускаем корутины
print(f"Время исполнения асинхронного парсера: {time.time() - start}")


# database.sort()
# with open("data.json", "w", encoding="utf-8") as out:
#     json.dump(database, out, indent="\t", ensure_ascii=False)


async_database.sort(key=lambda elem: elem["name"])
with open("async.json", "w", encoding="utf-8") as out:
    json.dump(async_database, out, indent="\t", ensure_ascii=False)
