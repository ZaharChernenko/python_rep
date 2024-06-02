import datetime
import os

from PyQt5 import QtWidgets
from PyQt5.QtGui import QFontDatabase, QIcon

import FilesTools
from AddMealWindow import AddMealWindow
from AddNewFoodWindow import AddNewFoodWindow
from EnterWindow import EnterWindow
from ListFoodWindow import ListFoodWindow
from MainWindow import MainWindow

"""
добавить приемы пищи
"""


def createEnterWindow():
    ui_enter_window = EnterWindow(enter_screen)
    ui_enter_window.btn_enter.clicked.connect(lambda: createMainWindow(*ui_enter_window.getValues()))
    ui_enter_window.burger_btn.clicked.connect(lambda: backToMainWindow())


def createMainWindow(calories, protein, fat, carb, date_time=datetime.date.today()):
    ui_main_window = MainWindow(enter_screen, calories, protein, fat, carb, date_time)
    ui_main_window.btn_add_food.clicked.connect(lambda: createListFoodWindow(ui_main_window.getDate(),
                                                                             dict_of_products))
    ui_main_window.burger_btn_2.clicked.connect(createEnterWindow)
    FilesTools.writeUserData(calories, protein, fat, carb)

    ui_main_window.prev_day_btn.clicked.connect(lambda: createMainWindow(calories, protein, fat, carb,
                                                                         ui_main_window.getDate() -
                                                                         datetime.timedelta(days=1)))

    ui_main_window.next_day_btn.clicked.connect(lambda: createMainWindow(calories, protein, fat, carb,
                                                                         ui_main_window.getDate() +
                                                                         datetime.timedelta(days=1)))


def backToMainWindow(date_time=datetime.date.today()):
    if os.path.isfile("./data/user_data.json"):
        back_user_data = FilesTools.readUserData()
        if back_user_data:
            createMainWindow(*back_user_data, date_time)


def createListFoodWindow(date_time, database):
    ui_list_food_window = ListFoodWindow(enter_screen, database)
    ui_list_food_window.burger_btn_3.clicked.connect(lambda: backToMainWindow(date_time))
    ui_list_food_window.btn_add_food.clicked.connect(
        lambda: createAddMealWindow(*ui_list_food_window.current_product, date_time))
    ui_list_food_window.btn_add_new_food.clicked.connect(lambda: createAddNewFoodWindow("", date_time))


def createAddNewFoodWindow(product_name, date_time):
    ui_add_new_food_window = AddNewFoodWindow(enter_screen, product_name, date_time)
    ui_add_new_food_window.widgetsWork(dict_of_products)
    ui_add_new_food_window.burger_btn_4.clicked.connect(
        lambda: createListFoodWindow(ui_add_new_food_window.getDate(), dict_of_products))
    ui_add_new_food_window.btn_add_food.clicked.connect(
        lambda: createListFoodWindow(ui_add_new_food_window.getDate(), dict_of_products))


def createAddMealWindow(product_name, calories, protein, fat, carbs, date_time):
    ui_add_meal_window = AddMealWindow(enter_screen, product_name, calories, protein, fat, carbs, date_time)
    ui_add_meal_window.burger_btn_4.clicked.connect(
        lambda: createListFoodWindow(ui_add_meal_window.getDate(), dict_of_products))

    ui_add_meal_window.btn_add_food.clicked.connect(lambda: backToMainWindow(date_time))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("img/burger-icon.png"))
    basedir = os.path.abspath(os.getcwd())
    regular_font_id = QFontDatabase.addApplicationFont(f"{basedir}/fonts/TTNormsPro-Regular.ttf")
    medium_font_id = QFontDatabase.addApplicationFont(f"{basedir}/fonts/TTNormsPro-Medium.ttf")
    enter_screen = QtWidgets.QMainWindow()
    enter_screen.setFixedSize(600, 900)
    dict_of_products = FilesTools.readFoodData()

    if not os.path.isfile("./data/user_data.json"):
        createEnterWindow()
        FilesTools.checkDirectory("./data/food_data")

    else:
        user_data = FilesTools.readUserData()
        if user_data:
            createMainWindow(*user_data)
        else:
            createEnterWindow()

    enter_screen.show()
    sys.exit(app.exec_())
