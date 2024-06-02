import json
import os


def isFileEmpty(file):
    with open(file, "r", encoding="utf-8") as fin:
        file_check = fin.read().strip()
        return file_check


def checkDirectory(path):
    try:
        path = path
        os.makedirs(path)

    except FileExistsError:
        print("Directory already exists")


def getValuesList(dictionary):
    return list(dictionary.values())


def readFoodData():
    with open("data/data.json", "r", encoding="utf-8") as fin:
        return json.load(fin)


def writeUserData(calories, protein, fat, carb):
    user_data_dict = {"calories": calories,
                      "protein": protein,
                      "fat": fat,
                      "carb": carb}
    with open("./data/user_data.json", "w", encoding="utf-8") as fout:
        json.dump(user_data_dict, fout, indent="\t", ensure_ascii=False)


def readUserData():
    file_check = isFileEmpty("./data/user_data.json")
    if file_check:
        try:
            user_check = json.loads(file_check, object_hook=getValuesList)
            for i in range(len(user_check)):
                user_check[i] = float(user_check[i])
            return tuple(user_check)[:4]

        except (json.JSONDecodeError, ValueError):
            print("user file was damaged")
            return False
    else:
        print("user file was damaged")
        return False
