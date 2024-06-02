import json
import locale
import os

from PyQt5 import QtCore, QtGui, QtWidgets

import setupUi
from FilesTools import isFileEmpty
from Meal import Meal
from Nutrients import Nutrients

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class MainWindow:
    def __init__(self, main_window, calories_aim_value, protein_aim_value,
                 fat_aim_value, carb_aim_value, date_time):

        self._calories_value: float = 0
        self._protein_value: float = 0
        self._fat_value: float = 0
        self._carb_value: float = 0

        self._calories_aim_value = calories_aim_value
        self._protein_aim_value = protein_aim_value
        self._fat_aim_value = fat_aim_value
        self._carb_aim_value = carb_aim_value

        self._date_time = date_time

        main_window.setStyleSheet("background-color: rgb(54, 54, 54);")
        self.centralwidget = QtWidgets.QWidget(main_window)

        medium_font = setupUi.setupMediumFont(30)

        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setGeometry(QtCore.QRect(0, 0, 600, 900))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_frame.sizePolicy().hasHeightForWidth())
        self.main_frame.setSizePolicy(sizePolicy)
        self.main_frame.setMinimumSize(QtCore.QSize(600, 900))
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.main_layout = QtWidgets.QVBoxLayout(self.main_frame)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.header = QtWidgets.QFrame(self.main_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy)
        self.header.setMinimumSize(QtCore.QSize(600, 89))
        self.header.setMaximumSize(QtCore.QSize(600, 89))
        self.header.setStyleSheet("border-bottom: 1px solid black;\n"
                                  "background-color: rgb(47, 47, 47);")
        self.header.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.header.setFrameShadow(QtWidgets.QFrame.Raised)

        self.header_layout = QtWidgets.QHBoxLayout(self.header)
        self.header_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.header_layout.setContentsMargins(20, 0, 20, 0)
        self.header_layout.addStretch(1)

        self.burger_btn_2 = setupUi.setupBurgerBtn(self.centralwidget)

        self.prev_day_btn = QtWidgets.QPushButton(self.header)
        self.prev_day_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.prev_day_btn.setStyleSheet("border: none;\n"
                                        "background-color: rgba(255, 255, 255, 0);")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("img/arrow-icon-left.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prev_day_btn.setIcon(icon2)
        self.prev_day_btn.setIconSize(QtCore.QSize(48, 48))
        self.header_layout.addWidget(self.prev_day_btn)

        self.label_data = QtWidgets.QLabel(self.header)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_data.sizePolicy().hasHeightForWidth())
        self.label_data.setSizePolicy(sizePolicy)
        self.label_data.setFont(medium_font)
        self.label_data.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "border: none;")
        self.label_data.setAlignment(QtCore.Qt.AlignCenter)
        self.label_data.setWordWrap(False)
        self.label_data.setText(self._date_time.strftime("%d %B").upper())
        self.header_layout.addWidget(self.label_data)

        self.next_day_btn = QtWidgets.QPushButton(self.header)
        self.next_day_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.next_day_btn.setStyleSheet("border: none;\n"
                                        "background-color: rgba(255, 255, 255, 0);")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("img/arrow-icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next_day_btn.setIcon(icon3)
        self.next_day_btn.setIconSize(QtCore.QSize(48, 48))
        self.header_layout.addWidget(self.next_day_btn)

        self.header_layout.setStretch(0, 1)
        self.header_layout.setStretch(2, 2)

        self.main_layout.addWidget(self.header)

        self.scroll_area = QtWidgets.QScrollArea(self.main_frame)
        self.scroll_area.setStyleSheet("border: none;")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.scroll_area_content = QtWidgets.QWidget()
        self.scroll_area_content.setGeometry(QtCore.QRect(0, 0, 583, 1031))

        self.scroll_area_content_vertical_layout = QtWidgets.QVBoxLayout(self.scroll_area_content)
        self.scroll_area_content_vertical_layout.setContentsMargins(20, 0, 0, 0)
        self.scroll_area_content_vertical_layout.setSpacing(11)

        self.nutrients_frame = QtWidgets.QFrame(self.scroll_area_content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nutrients_frame.sizePolicy().hasHeightForWidth())
        self.nutrients_frame.setSizePolicy(sizePolicy)
        self.nutrients_frame.setMinimumSize(QtCore.QSize(555, 410))
        self.nutrients_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.nutrients_frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self._food_list = []
        self._meals_list: list = []
        self.readValues()
        self.setProgress()
        self.checkProgress()

        self.calories_widget = Nutrients(parent=self.nutrients_frame,
                                         x=0, y=30,
                                         frame_width=541, height=77,
                                         progress_width=self._calories_progress,
                                         aim_value=self._calories_aim_value,
                                         current_value=self._calories_value,
                                         font_size=28, medium_font_size=34)
        self.calories_widget.frame.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
                                                 "border: 1px solid #B5A837;\n"
                                                 "border-radius: 8px;")
        self.calories_widget.background.setStyleSheet("background-color: #B5A837;\n"
                                                      "border: 1px solid #B5A837;\n"
                                                      "border-radius: 8px;")
        self.calories_widget.name_label.setText("калории")

        self.protein_widget = Nutrients(parent=self.nutrients_frame,
                                        x=0, y=137,
                                        frame_width=471, height=62,
                                        progress_width=self._protein_progress,
                                        aim_value=self._protein_aim_value,
                                        current_value=self._protein_value)
        self.protein_widget.frame.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
                                                "border: 1px solid #62D9C7;\n"
                                                "border-radius: 8px;")
        self.protein_widget.background.setStyleSheet("background-color: #62D9C7;\n"
                                                     "border: 1px solid #62D9C7;\n"
                                                     "border-radius: 8px;")
        self.protein_widget.name_label.setText("белки")

        self.fat_widget = Nutrients(parent=self.nutrients_frame,
                                    x=0, y=229,
                                    frame_width=411, height=62,
                                    progress_width=self._fat_progress,
                                    aim_value=self._fat_aim_value,
                                    current_value=self._fat_value)
        self.fat_widget.frame.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
                                            "border: 1px solid #F59705;\n"
                                            "border-radius: 8px;")
        self.fat_widget.background.setStyleSheet("background-color: #F59705;\n"
                                                 "border: 1px solid #F59705;\n"
                                                 "border-radius: 8px;")
        self.fat_widget.name_label.setText("жиры")

        self.carb_widget = Nutrients(self.nutrients_frame,
                                     x=0, y=321,
                                     frame_width=501, height=62,
                                     progress_width=self._carb_progress,
                                     aim_value=self._carb_aim_value,
                                     current_value=self._carb_value)
        self.carb_widget.frame.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
                                             "border: 1px solid #D762D9;\n"
                                             "border-radius: 8px;")
        self.carb_widget.background.setStyleSheet("background-color: #D762D9;\n"
                                                  "border: 1px solid #D762D9;\n"
                                                  "border-radius: 8px;")
        self.carb_widget.name_label.setText("углеводы")

        self.scroll_area_content_vertical_layout.addWidget(self.nutrients_frame)

        for food in self._meals_list:
            self.scroll_area_content_vertical_layout.addWidget(food)

        spacerItem5 = QtWidgets.QSpacerItem(20, 150, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.MinimumExpanding)
        self.scroll_area_content_vertical_layout.addItem(spacerItem5)
        self.scroll_area.setWidget(self.scroll_area_content)
        self.main_layout.addWidget(self.scroll_area)

        self.btn_add_food = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add_food.setGeometry(QtCore.QRect(460, 770, 102, 102))
        self.btn_add_food.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_food.setStyleSheet("border: none;\n"
                                        "background-color: rgba(255, 255, 255, 0);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/add_food-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add_food.setIcon(icon)
        self.btn_add_food.setIconSize(QtCore.QSize(102, 102))

        main_window.setCentralWidget(self.centralwidget)
        main_window.setWindowTitle("Калькулятор калорий")
        QtCore.QMetaObject.connectSlotsByName(main_window)

        self.mealsWork()

    def getTime(self, dictionary):
        return dictionary["time"]

    def readValues(self):
        if os.path.isfile(f"data/food_data/{self._date_time}.json"):
            file_check = isFileEmpty(f"data/food_data/{self._date_time}.json")
            if file_check:
                self._food_list = json.loads(file_check)
                self._food_list.sort(key=self.getTime)
                for food in self._food_list:
                    self._calories_value += float(food["calories"])
                    self._protein_value += float(food["protein"])
                    self._fat_value += float(food["fat"])
                    self._carb_value += float(food["carb"])
                    self._meals_list.append(Meal(self.scroll_area_content, *food.values()))

                self._calories_value = round(self._calories_value, 1)
                self._protein_value = round(self._protein_value, 1)
                self._fat_value = round(self._fat_value, 1)
                self._carb_value = round(self._carb_value, 1)

    def setProgress(self):
        self._calories_progress = int(min(self._calories_value / self._calories_aim_value, 1) * 551)

        if self._protein_aim_value != 0:
            self._protein_progress = int(min(self._protein_value / self._protein_aim_value, 1) * 471)
        else:
            self._protein_progress = 471

        if self._fat_aim_value != 0:
            self._fat_progress = int(min(self._fat_value / self._fat_aim_value, 1) * 411)
        else:
            self._fat_progress = 411

        if self._carb_aim_value != 0:
            self._carb_progress = int(min(self._carb_value / self._carb_aim_value, 1) * 501)
        else:
            self._carb_progress = 501

    def checkProgress(self):
        if self._calories_progress < 20:
            self._calories_progress = 0
        if self._protein_progress < 20:
            self._protein_progress = 0
        if self._fat_progress < 20:
            self._fat_progress = 0
        if self._carb_progress < 20:
            self._carb_progress = 0

    def getDate(self):
        return self._date_time

    def deleteMeal(self, meal):
        for elem in self._food_list:
            if meal.time_label.text() in elem.values() and meal.name in elem.values() and meal.weight in elem.values():

                self._calories_value = round(self._calories_value - meal.calories, 1)
                self._protein_value = round(self._protein_value - meal.protein, 1)
                self._fat_value = round(self._fat_value - meal.fat, 1)
                self._carb_value = round(self._carb_value - meal.carb, 1)
                self.setProgress()
                self.checkProgress()
                self.calories_widget.changeNutrient(0, 30, self._calories_progress, 77, self._calories_value)
                self.protein_widget.changeNutrient(0, 137, self._protein_progress, 62, self._protein_value)
                self.fat_widget.changeNutrient(0, 229, self._fat_progress, 62, self._fat_value)
                self.carb_widget.changeNutrient(0, 321, self._carb_progress, 62, self._carb_value)

                meal.deleteLater()
                self._meals_list.remove(meal)
                self._food_list.remove(elem)
                file = f"data/food_data/{self._date_time}.json"
                with open(file, "w", encoding="utf-8") as fout:
                    json.dump(self._food_list, fout, indent="\t", ensure_ascii=False)
                break

    def mealsWork(self):
        for meal in self._meals_list:
            meal.delete_food_btn.released.connect(lambda x=meal: self.deleteMeal(x))
