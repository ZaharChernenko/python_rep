from PyQt5 import QtCore, QtGui, QtWidgets

import setupUi
from Input import InputParameters


class EnterWindow(object):
    def __init__(self, enter_window):

        enter_window.setStyleSheet("background-color: rgb(54, 54, 54);")
        self.central_widget = QtWidgets.QWidget(enter_window)

        font = setupUi.setupRegularFont(28)
        medium_font = setupUi.setupMediumFont(30)

        self.header = setupUi.setupHeader(self.central_widget)
        self.header.setFont(medium_font)
        self.burger_btn = setupUi.setupBurgerBtn(self.central_widget)

        self.label = QtWidgets.QLabel(self.central_widget)
        self.label.setGeometry(QtCore.QRect(20, 127, 199, 40))
        medium_font.setPointSize(28)
        self.label.setFont(medium_font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.radio_female = QtWidgets.QRadioButton(self.central_widget)
        self.radio_female.setGeometry(QtCore.QRect(20, 207, 199, 40))
        self.radio_female.setFont(font)
        self.radio_female.setStyleSheet("padding-left: 2px;\n"
                                        "color: rgb(255, 255, 255);")

        self.radio_male = QtWidgets.QRadioButton(self.central_widget)
        self.radio_male.setGeometry(QtCore.QRect(20, 167, 199, 41))
        self.radio_male.setFont(font)
        self.radio_male.setStyleSheet("padding-left: 2px;\n"
                                      "color: rgb(255, 255, 255);")

        self._input_weight = InputParameters(self.central_widget, 20, 277, 210, 40, "Вес: ", False, False)
        self._input_height = InputParameters(self.central_widget, 20, 347, 210, 40, "Рост: ", False, False)
        self._input_age = InputParameters(self.central_widget, 20, 417, 210, 40, "Возраст: ", True, False)

        self.label_activity = QtWidgets.QLabel(self.central_widget)
        self.label_activity.setGeometry(QtCore.QRect(20, 487, 211, 40))
        font.setPointSize(28)
        self.label_activity.setFont(font)
        self.label_activity.setStyleSheet("color: rgb(255, 255, 255);")

        self.combo_box_activity = QtWidgets.QComboBox(self.central_widget)
        self.combo_box_activity.setGeometry(QtCore.QRect(20, 532, 530, 40))
        font.setPointSize(18)
        self.combo_box_activity.setFont(font)
        self.combo_box_activity.setStyleSheet("color: rgb(255, 255, 255);\n"
                                              "border: 1px solid white;\n"
                                              "border: 1px solid white;\n"
                                              "border-radius: 2px")

        self.combo_box_activity.addItem("")
        self.combo_box_activity.addItem("")
        self.combo_box_activity.addItem("")
        self.combo_box_activity.addItem("")
        self.combo_box_activity.addItem("")

        self.label_aim = QtWidgets.QLabel(self.central_widget)
        self.label_aim.setGeometry(QtCore.QRect(20, 602, 199, 40))
        font.setPointSize(28)
        self.label_aim.setFont(font)
        self.label_aim.setStyleSheet("color: rgb(255, 255, 255);")

        self.combo_box_aim = QtWidgets.QComboBox(self.central_widget)
        self.combo_box_aim.setGeometry(QtCore.QRect(20, 647, 530, 40))
        font.setPointSize(18)
        self.combo_box_aim.setFont(font)
        self.combo_box_aim.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "border: 1px solid white;\n"
                                         "border-radius: 2px")
        self.combo_box_aim.addItem("")
        self.combo_box_aim.addItem("")
        self.combo_box_aim.addItem("")

        self.btn_calc = QtWidgets.QPushButton(self.central_widget)
        self.btn_calc.setGeometry(QtCore.QRect(110, 750, 100, 100))
        self.btn_calc.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_calc.setStyleSheet("border: none;\n"
                                    "background-color: rgba(255, 255, 255, 0);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("img/calculator-icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btn_calc.setIcon(icon1)
        self.btn_calc.setIconSize(QtCore.QSize(100, 100))
        self.btn_calc.setObjectName("btn_calc")

        self.btn_enter = QtWidgets.QPushButton(self.central_widget)
        self.btn_enter.setGeometry(QtCore.QRect(387, 746, 108, 108))
        self.btn_enter.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_enter.setStyleSheet("border: none;\n"
                                     "background-color: rgba(255, 255, 255, 0);")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("img/arrow-first-icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btn_enter.setIcon(icon2)
        self.btn_enter.setIconSize(QtCore.QSize(108, 108))

        self._input_calories = InputParameters(self.central_widget, 300, 127, 280, 40, "Калории: ", False, True)
        self._input_calories.setStyleSheet("color: rgb(181, 168, 55);\n"
                                           "border: 1px solid #b5a837;\n"
                                           "border-radius: 2px")

        self._input_protein = InputParameters(self.central_widget, 310, 207, 270, 40, "Белки: ", False, True)
        self._input_protein.setStyleSheet("color: rgb(98, 217, 199);\n"
                                          "border: 1px solid #62d9c7;\n"
                                          "border-radius: 2px")

        self._input_fat = InputParameters(self.central_widget, 310, 287, 270, 40, "Жиры: ", False, True)
        self._input_fat.setStyleSheet("color: rgb(245, 151, 5);\n"
                                      "border: 1px solid #f59705;\n"
                                      "border-radius: 2px")

        self._input_carb = InputParameters(self.central_widget, 310, 367, 270, 40, "Углеводы: ", False, True)
        self._input_carb.setStyleSheet("color: rgb(215, 98, 217);\n"
                                       "border: 1px solid #d762d9;\n"
                                       "border-radius: 2px")

        enter_window.setCentralWidget(self.central_widget)

        self.retranslateUi(enter_window)
        self.btn_calc.setDisabled(True)
        self.btn_enter.setDisabled(True)
        self.widgetsWork()

        QtCore.QMetaObject.connectSlotsByName(enter_window)

    def retranslateUi(self, enter_window):
        _translate = QtCore.QCoreApplication.translate
        enter_window.setWindowTitle(_translate("MainWindow", "Подсчет калорий"))
        self.header.setText(_translate("MainWindow", "ПОДСЧЕТ КАЛОРИЙ"))
        self.radio_female.setText(_translate("MainWindow", "женский"))
        self.radio_male.setText(_translate("MainWindow", "мужской"))
        self.combo_box_activity.setCurrentText(_translate("MainWindow", "Маленькая активность"))
        self.combo_box_activity.setItemText(0, _translate("MainWindow", "Маленькая активность"))
        self.combo_box_activity.setItemText(1, _translate("MainWindow", "Легкая активность (1-3 тренировки в неделю)"))
        self.combo_box_activity.setItemText(2, _translate("MainWindow", "Средняя активность (3-5)"))
        self.combo_box_activity.setItemText(3, _translate("MainWindow", "Большая активность (6-7)"))
        self.combo_box_activity.setItemText(4, _translate("MainWindow", "Очень большая активность (>7)"))
        self.label_activity.setText(_translate("MainWindow", "Активность:"))
        self.combo_box_aim.setCurrentText(_translate("MainWindow", "Сбросить вес"))
        self.combo_box_aim.setItemText(0, _translate("MainWindow", "Сбросить вес"))
        self.combo_box_aim.setItemText(1, _translate("MainWindow", "Поддерживать вес"))
        self.combo_box_aim.setItemText(2, _translate("MainWindow", "Набрать мышцы"))
        self.label_aim.setText(_translate("MainWindow", "Цель:"))
        self.label.setText(_translate("MainWindow", "Пол:"))
        self._input_protein.setText(_translate("MainWindow", "Белки: "))
        self._input_calories.setText(_translate("MainWindow", "Калории: "))
        self._input_fat.setText(_translate("MainWindow", "Жиры: "))
        self._input_carb.setText(_translate("MainWindow", "Углеводы: "))

    def getValues(self):
        return (self._input_calories.value, self._input_protein.value,
                self._input_fat.value, self._input_carb.value)

    def checkValidToCalc(self):
        self.btn_calc.setEnabled(
            self._input_weight.is_valid and self._input_age.is_valid and self._input_height.is_valid and (
                self.radio_male.isChecked() or self.radio_female.isChecked()))

    def calculate(self):
        multipliers_of_activity = [1.2, 1.375, 1.55, 1.725, 1.9]
        multipliers_of_aim = [0.8, 1, 1.1]
        if self.radio_male.isChecked():
            BMR = 88.4 + (13.4 * self._input_weight.value) + (4.8 * self._input_height.value) - (
                5.7 * self._input_age.value)
        else:
            BMR = 445.6 + (9.2 * self._input_weight.value) + (3 * self._input_height.value) - (
                4.3 * self._input_age.value)
        self._input_calories.value = round(
            BMR * multipliers_of_activity[self.combo_box_activity.currentIndex()] * multipliers_of_aim[
                self.combo_box_aim.currentIndex()], 1)
        self._input_protein.value = round(self._input_calories.value * 0.3 / 4, 1)
        self._input_carb.value = round(self._input_calories.value * 0.4 / 4, 1)
        self._input_fat.value = round(self._input_calories.value * 0.3 / 9, 1)

        self._input_calories.is_valid = True
        self._input_protein.is_valid = True
        self._input_carb.is_valid = True
        self._input_fat.is_valid = True

        self._input_calories.setText(self._input_calories.getOriginalText() + str(self._input_calories.value))
        self._input_protein.setText(self._input_protein.getOriginalText() + str(self._input_protein.value))
        self._input_carb.setText(self._input_carb.getOriginalText() + str(self._input_carb.value))
        self._input_fat.setText(self._input_fat.getOriginalText() + str(self._input_fat.value))

        self.btn_enter.setEnabled(True)

    def checkNutrients(self):
        new_input_calories_value = round(
            self._input_protein.value * 4 + self._input_fat.value * 9 + self._input_carb.value * 4, 1)
        if new_input_calories_value > self._input_calories.value:
            self._input_calories.value = new_input_calories_value
            self._input_calories.setText(self._input_calories.getOriginalText() + str(self._input_calories.value))
        if self._input_calories.is_valid and (
                self._input_carb.is_valid + self._input_fat.is_valid + self._input_protein.is_valid) >= 2:
            self.btn_enter.setEnabled(True)
        else:
            self.btn_enter.setEnabled(False)

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

    def widgetsWork(self):
        self.radio_male.toggled.connect(self.checkValidToCalc)
        self.radio_female.toggled.connect(self.checkValidToCalc)

        self._input_weight.textEdited.connect(lambda: self._input_weight.changeText())
        self._input_weight.textEdited.connect(lambda: self._input_weight.checkValid(700, 30))
        self._input_weight.textEdited.connect(self.checkValidToCalc)

        self._input_height.textEdited.connect(lambda: self._input_height.changeText())
        self._input_height.textEdited.connect(lambda: self._input_height.checkValid(270, 100))
        self._input_height.textEdited.connect(self.checkValidToCalc)

        self._input_age.textEdited.connect(lambda: self._input_age.changeText())
        self._input_age.textEdited.connect(lambda: self._input_age.checkValid(130, 12))
        self._input_age.textEdited.connect(self.checkValidToCalc)

        self._input_calories.textEdited.connect(lambda: self._input_calories.changeText(-1))
        self._input_calories.textChanged.connect(lambda: self._input_calories.checkValid(9999, 700))
        self._input_calories.textEdited.connect(lambda: self.resetPFC())

        self._input_protein.textEdited.connect(lambda: self._input_protein.changeText())
        self._input_protein.textEdited.connect(lambda: self._input_protein.checkValid(1000, 0))
        self._input_protein.textChanged.connect(self.checkNutrients)

        self._input_fat.textEdited.connect(lambda: self._input_fat.changeText())
        self._input_fat.textEdited.connect(lambda: self._input_fat.checkValid(1000, 0))
        self._input_fat.textChanged.connect(self.checkNutrients)

        self._input_carb.textEdited.connect(lambda: self._input_carb.changeText())
        self._input_carb.textEdited.connect(lambda: self._input_carb.checkValid(1000, 0))
        self._input_carb.textChanged.connect(self.checkNutrients)

        self.btn_calc.clicked.connect(lambda: self.calculate())
