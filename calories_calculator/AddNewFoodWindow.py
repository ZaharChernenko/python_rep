import json

from PyQt5 import QtCore, QtGui, QtWidgets

import setupUi
from Input import InputParameters


class AddNewFoodWindow:
    def __init__(self, add_food_weight_window, product_name, date_time):
        self._date_time = date_time
        self._is_available_name = False
        self._is_correct_nutrients = False
        add_food_weight_window.setStyleSheet("background-color: rgb(54, 54, 54);")
        self.central_widget = QtWidgets.QWidget(add_food_weight_window)

        font = setupUi.setupRegularFont(22)
        medium_font = setupUi.setupMediumFont(30)

        self.header = setupUi.setupHeader(self.central_widget)
        self.header.setFont(medium_font)

        self.burger_btn_4 = setupUi.setupBurgerBtn(self.central_widget)

        self._input_product_name = QtWidgets.QLineEdit(self.central_widget)
        self._input_product_name.setGeometry(QtCore.QRect(209, 127, 361, 50))
        self._input_product_name.setFont(font)
        self._input_product_name.setText(product_name)
        self._input_product_name.setStyleSheet("padding-left: 10px;\n"
                                               "color: rgb(255, 255, 255);\n"
                                               "border: 1px solid white;\n"
                                               "border-radius: 2px")

        self._input_weight = InputParameters(self.central_widget, 209, 207, 170, 50, "", False, False, True)
        self._input_weight.setAlignment(QtCore.Qt.AlignCenter)
        self._input_weight.value = 100

        self._input_calories = InputParameters(self.central_widget, 209, 287, 170, 50, "", False, True)
        self._input_calories.setAlignment(QtCore.Qt.AlignCenter)
        self._input_calories.setStyleSheet("color: rgb(181, 168, 55);\n"
                                           "border: 1px solid #b5a837;\n"
                                           "border-radius: 2px")

        self._input_protein = InputParameters(self.central_widget, 209, 367, 170, 50, "", False, True)
        self._input_protein.setAlignment(QtCore.Qt.AlignCenter)
        self._input_protein.setStyleSheet("color: rgb(98, 217, 199);\n"
                                          "border: 1px solid #62d9c7;\n"
                                          "border-radius: 2px")

        self._input_fat = InputParameters(self.central_widget, 209, 447, 170, 50, "", False, True)
        self._input_fat.setAlignment(QtCore.Qt.AlignCenter)
        self._input_fat.setStyleSheet("color: rgb(245, 151, 5);\n"
                                      "border: 1px solid #f59705;\n"
                                      "border-radius: 2px")

        self._input_carb = InputParameters(self.central_widget, 209, 527, 170, 50, "", False, True)
        self._input_carb.setAlignment(QtCore.Qt.AlignCenter)
        self._input_carb.setStyleSheet("color: rgb(215, 98, 217);\n"
                                       "border: 1px solid #d762d9;\n"
                                       "border-radius: 2px")

        font.setPointSize(26)
        self.label_product = QtWidgets.QLabel(self.central_widget)
        self.label_product.setGeometry(QtCore.QRect(20, 127, 161, 50))
        self.label_product.setFont(font)
        self.label_product.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_product.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.label_weight = QtWidgets.QLabel(self.central_widget)
        self.label_weight.setGeometry(QtCore.QRect(20, 207, 161, 50))
        self.label_weight.setFont(font)
        self.label_weight.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_weight.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.label_calories = QtWidgets.QLabel(self.central_widget)
        self.label_calories.setGeometry(QtCore.QRect(20, 287, 161, 50))
        self.label_calories.setFont(font)
        self.label_calories.setStyleSheet("color: rgb(181, 168, 55);")
        self.label_calories.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.label_protein = QtWidgets.QLabel(self.central_widget)
        self.label_protein.setGeometry(QtCore.QRect(20, 367, 161, 50))
        self.label_protein.setFont(font)
        self.label_protein.setStyleSheet("color: rgb(98, 217, 199);")
        self.label_protein.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.label_fat = QtWidgets.QLabel(self.central_widget)
        self.label_fat.setGeometry(QtCore.QRect(20, 447, 161, 50))
        self.label_fat.setFont(font)
        self.label_fat.setStyleSheet("color: rgb(245, 151, 5);")
        self.label_fat.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.label_carb = QtWidgets.QLabel(self.central_widget)
        self.label_carb.setGeometry(QtCore.QRect(20, 527, 161, 50))
        self.label_carb.setFont(font)
        self.label_carb.setStyleSheet("color: rgb(215, 98, 217);")
        self.label_carb.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.btn_add_food = QtWidgets.QPushButton(self.central_widget)
        self.btn_add_food.setGeometry(QtCore.QRect(446, 746, 100, 100))
        self.btn_add_food.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_food.setStyleSheet("border: none;\n"
                                        "background-color: rgba(255, 255, 255, 0);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("img/plus-icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add_food.setIcon(icon1)
        self.btn_add_food.setIconSize(QtCore.QSize(100, 100))
        self.btn_add_food.setDisabled(True)
        add_food_weight_window.setCentralWidget(self.central_widget)

        self.inputWeightWork()

        self.retranslateUi(add_food_weight_window)
        QtCore.QMetaObject.connectSlotsByName(add_food_weight_window)

    def retranslateUi(self, add_new_food_window):
        _translate = QtCore.QCoreApplication.translate
        add_new_food_window.setWindowTitle(_translate("AddFoodWeightWindow", "Добавить новый продукт"))
        self.header.setText(_translate("AddFoodWeightWindow", "ДОБАВИТЬ ПРОДУКТ"))
        self.label_product.setText(_translate("AddFoodWeightWindow", "Продукт:"))
        self.label_weight.setText(_translate("AddFoodWeightWindow", "Вес, г:"))
        self.label_calories.setText(_translate("AddFoodWeightWindow", "Калории:"))
        self.label_protein.setText(_translate("AddFoodWeightWindow", "Белки:"))
        self.label_fat.setText(_translate("AddFoodWeightWindow", "Жиры:"))
        self.label_carb.setText(_translate("AddFoodWeightWindow", "Углеводы:"))
        self._input_weight.setPlaceholderText("100")

    def getDate(self):
        return self._date_time

    def checkIsAvailableName(self, dict_of_products):
        self._input_product_name.setText(self._input_product_name.text().lstrip())
        self._is_available_name = True
        if self._input_product_name.text() == "":
            self._is_available_name = False
        else:
            for product in dict_of_products:
                if self._input_product_name.text().lower() == product["name"].lower():
                    self._is_available_name = False
                    self._input_product_name.setStyleSheet("padding-left: 10px;\n"
                                                           "color: rgb(255, 255, 255);\n"
                                                           "border: 1px solid #f59705;\n"
                                                           "border-radius: 2px")
                    break
            if self._is_available_name:
                self._input_product_name.setStyleSheet("padding-left: 10px;\n"
                                                       "color: rgb(255, 255, 255);\n"
                                                       "border: 1px solid white;\n"
                                                       "border-radius: 2px")
        self.btn_add_food.setEnabled(self._is_available_name and self._is_correct_nutrients)

    def checkNutrients(self):
        new_input_calories_value = round(
            self._input_protein.value * 4 + self._input_fat.value * 9 + self._input_carb.value * 4, 1)
        if new_input_calories_value > self._input_calories.value:
            self._input_calories.value = new_input_calories_value
            self._input_calories.setText(self._input_calories.getOriginalText() + str(self._input_calories.value))

        if (self._input_carb.is_valid + self._input_fat.is_valid + self._input_protein.is_valid) >= 1 and (
                self._input_protein.value + self._input_fat.value + self._input_carb.value <= self._input_weight.value):
            self._is_correct_nutrients = True
        else:
            self._is_correct_nutrients = False

        self.btn_add_food.setEnabled(self._is_available_name and self._is_correct_nutrients)

    def resetPFC(self):
        self._input_protein.setText(self._input_protein.getOriginalText())
        self._input_protein.value = 0
        self._input_protein.is_valid = False
        self._input_fat.setText(self._input_fat.getOriginalText())
        self._input_fat.value = 0
        self._input_fat.is_valid = False
        self._input_carb.setText(self._input_carb.getOriginalText())
        self._input_carb.value = 0
        self._input_carb.is_valid = False

    def writeNewFood(self, list_of_products):
        self._input_product_name.setText((self._input_product_name.text()[0].upper() +
                                          self._input_product_name.text()[1:]).rstrip())

        index = 0
        while index < len(list_of_products) and self._input_product_name.text() > list_of_products[index]["name"]:
            index += 1
        list_of_products.insert(index, {"name": self._input_product_name.text(),
                                        "calories": round(self._input_calories.value / self._input_weight.value * 100,
                                                          1),
                                        "protein": round(self._input_protein.value / self._input_weight.value * 100, 1),
                                        "fat": round(self._input_fat.value / self._input_weight.value * 100, 1),
                                        "carb": round(self._input_carb.value / self._input_weight.value * 100, 1)})

        with open("data/data.json", "w", encoding="utf-8") as fout:
            json.dump(list_of_products, fout, indent="\t", ensure_ascii=False)

    def inputWeightWork(self):
        self._input_weight.textEdited.connect(lambda: self._input_weight.changeText(-1))
        self._input_weight.textEdited.connect(lambda: self._input_weight.checkValid(999, 0, 100))
        self._input_weight.textEdited.connect(lambda: self._input_weight.setAlignment(QtCore.Qt.AlignCenter))

    def widgetsWork(self, list_of_products):
        self._input_product_name.textEdited.connect(lambda: self.checkIsAvailableName(list_of_products))

        self._input_weight.textEdited.connect(lambda: self.checkNutrients())

        self._input_calories.textEdited.connect(lambda: self._input_calories.changeText(-1))
        self._input_calories.textChanged.connect(lambda: self._input_calories.checkValid(9999, 0))
        self._input_calories.textEdited.connect(lambda: self.resetPFC())
        self._input_calories.textEdited.connect(lambda: self._input_calories.setAlignment(QtCore.Qt.AlignCenter))

        self._input_protein.textEdited.connect(lambda: self._input_protein.changeText())
        self._input_protein.textEdited.connect(lambda: self._input_protein.checkValid(999, 0))
        self._input_protein.textChanged.connect(lambda: self.checkNutrients())
        self._input_protein.textEdited.connect(lambda: self._input_protein.setAlignment(QtCore.Qt.AlignCenter))

        self._input_fat.textEdited.connect(lambda: self._input_fat.changeText())
        self._input_fat.textEdited.connect(lambda: self._input_fat.checkValid(999, 0))
        self._input_fat.textChanged.connect(lambda: self.checkNutrients())
        self._input_fat.textEdited.connect(lambda: self._input_fat.setAlignment(QtCore.Qt.AlignCenter))

        self._input_carb.textEdited.connect(lambda: self._input_carb.changeText())
        self._input_carb.textEdited.connect(lambda: self._input_carb.checkValid(999, 0))
        self._input_carb.textChanged.connect(lambda: self.checkNutrients())
        self._input_carb.textEdited.connect(lambda: self._input_carb.setAlignment(QtCore.Qt.AlignCenter))

        self.btn_add_food.clicked.connect(lambda: self.writeNewFood(list_of_products))
