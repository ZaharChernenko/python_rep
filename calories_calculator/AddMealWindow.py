import json
import os

from PyQt5.QtCore import QRect, Qt, QTime
from PyQt5.QtWidgets import QLabel, QTimeEdit

from AddNewFoodWindow import AddNewFoodWindow
from FilesTools import isFileEmpty
from setupUi import setupRegularFont


class AddMealWindow(AddNewFoodWindow):
    def __init__(self, add_meal_window, product_name, calories, protein, fat, carb, date_time):
        super().__init__(add_meal_window, product_name, date_time)
        font = setupRegularFont(22)
        self._calories = float(calories)
        self._protein = float(protein)
        self._fat = float(fat)
        self._carb = float(carb)

        self._input_product_name.setReadOnly(True)
        self._input_calories.setReadOnly(True)
        self._input_protein.setReadOnly(True)
        self._input_fat.setReadOnly(True)
        self._input_carb.setReadOnly(True)

        self.label_time = QLabel(self.central_widget)
        self.label_time.setGeometry(QRect(20, 607, 161, 50))
        font.setPointSize(26)
        self.label_time.setFont(font)
        self.label_time.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_time.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.label_time.setText("Время:")

        self.time_input = QTimeEdit(self.central_widget)
        self.time_input.setGeometry(QRect(209, 607, 170, 50))
        font.setPointSize(25)
        self.time_input.setFont(font)
        self.time_input.setStyleSheet("color: white;\n")
        self.time_input.setAlignment(Qt.AlignCenter)
        self.time_input.setTime(QTime.currentTime())

        self._input_calories.setText(str(self._calories))
        self._input_protein.setText(str(self._protein))
        self._input_fat.setText(str(self._fat))
        self._input_carb.setText(str(self._carb))

        self._input_weight.textEdited.connect(self.calculate)
        self.btn_add_food.setEnabled(True)
        self.btn_add_food.clicked.connect(self.addMeal)

        add_meal_window.setWindowTitle("Добавить прием пищи")

    def calculate(self):
        if self._input_weight.text() != "":
            self._input_calories.setText(str(round(float(self._input_weight.text()) / 100 * self._calories, 1)))
            self._input_protein.setText(str(round(float(self._input_weight.text()) / 100 * self._protein, 1)))
            self._input_fat.setText(str(round(float(self._input_weight.text()) / 100 * self._fat, 1)))
            self._input_carb.setText(str(round(float(self._input_weight.text()) / 100 * self._carb, 1)))
        else:
            self._input_calories.setText(str(self._calories))
            self._input_protein.setText(str(self._protein))
            self._input_fat.setText(str(self._fat))
            self._input_carb.setText(str(self._carb))

        self._input_calories.setAlignment(Qt.AlignCenter)
        self._input_protein.setAlignment(Qt.AlignCenter)
        self._input_fat.setAlignment(Qt.AlignCenter)
        self._input_carb.setAlignment(Qt.AlignCenter)

    def addMeal(self):

        if not self._input_weight.text():
            weight: float = 100
            calories = self._calories
            protein = self._protein
            fat = self._fat
            carb = self._carb
        else:
            weight = float(self._input_weight.text())
            calories = float(self._input_calories.text())
            protein = float(self._input_protein.text())
            fat = float(self._input_fat.text())
            carb = float(self._input_carb.text())

        food_data_dict = {"time": self.time_input.time().toString()[0:5],
                          "name": self._input_product_name.text(),
                          "weight": weight,
                          "calories": calories,
                          "protein": protein,
                          "fat": fat,
                          "carb": carb}

        file = f"data/food_data/{self.getDate()}.json"
        if os.path.isfile(file):
            file_check = isFileEmpty(file)
            if file_check:
                food_data_list = json.loads(file_check)
                food_data_list.append(food_data_dict)
            else:
                food_data_list = [food_data_dict]

        else:
            food_data_list = [food_data_dict]

        with open(file, "w", encoding="utf-8") as fout:
            json.dump(food_data_list, fout, indent="\t", ensure_ascii=False)
