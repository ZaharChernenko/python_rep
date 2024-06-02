from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QLineEdit

from setupUi import setupRegularFont


class InputParameters(QLineEdit):

    def __init__(self, window, x, y, width, height, name, age, nutrients, product_weight=False):
        super().__init__(window)
        self.is_valid = False
        self.value: float = 0
        self._original_text = name
        self._is_age = age
        self._is_nutrients = nutrients
        self._is_product_weight = product_weight

        self.setGeometry(QRect(x, y, width, height))
        font = setupRegularFont(25)
        self.setFont(font)
        self.setStyleSheet("color: rgb(255, 255, 255);\n"
                           "border: 1px solid white;\n"
                           "border-radius: 2px")
        self.setText(name)

    def changeText(self, exp=0):
        if self.text()[:len(self._original_text)] != self._original_text:  # запрет на изменение названий input'ов
            self.setText(self._original_text)

        if len(self.text()) - len(self._original_text) == 1 and self.text()[-1] == "0" and not self._is_nutrients:
            self.setText(self.text()[:-1])

        self.checkNumber(len(self._original_text), exp, 0, False, self._is_age)

    def checkNumber(self, i, exp, mant, point, age):
        count_exponent = exp
        count_mantissa = mant
        is_point = point
        if i == len(self.text()):
            return

        if self.text()[i].isdigit():
            if count_exponent == 3 and not is_point:
                self.setText(self.text()[:i] + self.text()[i + 1:])
                self.checkNumber(i, count_exponent, count_mantissa, is_point, age)
            elif count_exponent < 3 and not is_point:
                count_exponent += 1
                self.checkNumber(i + 1, count_exponent, count_mantissa, is_point, age)
            elif count_mantissa == 1:
                self.setText(self.text()[:i] + self.text()[i + 1:])
                self.checkNumber(i, count_exponent, count_mantissa, is_point, age)
            elif count_mantissa < 1 and is_point:
                count_mantissa += 1
                self.checkNumber(i + 1, count_exponent, count_mantissa, is_point, age)

        else:
            if self.text()[i] == "." and not is_point and not age and i != len(self._original_text):
                self.checkNumber(i + 1, count_exponent, count_mantissa, True, age)
            else:
                self.setText(self.text()[:i] + self.text()[i + 1:])
                self.checkNumber(i, count_exponent, count_mantissa, is_point, age)

    def checkValid(self, max_limit, min_limit, reset_value=0):
        if self.text()[len(self._original_text):] == "" or float(
            self.text()[len(self._original_text):]) > max_limit or float(
                self.text()[len(self._original_text):]) <= min_limit:
            self.is_valid = False
            if not self._is_nutrients and not self._is_product_weight:
                self.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "border: 1px solid #f59705;\n"
                                   "border-radius: 2px")
            else:
                self.value = reset_value
        else:
            self.is_valid = True
            self.value = float(self.text()[len(self._original_text):])
            if not self._is_nutrients:
                self.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "border: 1px solid white;\n"
                                   "border-radius: 2px")

    def getOriginalText(self):
        return self._original_text
