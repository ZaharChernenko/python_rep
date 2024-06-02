from PyQt5 import QtCore
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QSizePolicy,
                             QSpacerItem)

import setupUi


class Nutrients:
    def __init__(self, parent, x, y, frame_width, height, progress_width, aim_value, current_value,
                 font_size=24, medium_font_size=29):
        self._current_value = current_value
        self._aim_value = aim_value

        font = setupUi.setupRegularFont(font_size)
        medium_font = setupUi.setupMediumFont(medium_font_size)

        self.background = QFrame(parent)
        self.background.setGeometry(QtCore.QRect(x, y, progress_width, height))
        self.background.setFrameShape(QFrame.StyledPanel)
        self.background.setFrameShadow(QFrame.Raised)

        self.frame = QFrame(parent)
        self.frame.setGeometry(QtCore.QRect(x, y, frame_width, height))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.name_label = QLabel(self.frame)
        self.name_label.setFont(medium_font)
        self.name_label.setStyleSheet("border: none;\n"
                                      "background-color: rgba(255, 255, 255, 0);\n"
                                      "color: white;")
        self.name_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.label = QLabel(self.frame)
        self.label.setFont(font)
        self.label.setStyleSheet("border: none;\n"
                                 "background-color: rgba(255, 255, 255, 0);\n"
                                 "color: white;")
        if self._current_value > self._aim_value:
            self.label.setStyleSheet("color: red")
        self.label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label.setText(f"{str(self._current_value)}/{str(self._aim_value)}")

        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(10, 9, -1, 9)
        self.horizontalLayout.addWidget(self.name_label)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.label)

    def changeNutrient(self, x, y, progress_width, height, current_value):
        self._current_value = current_value
        self.background.setGeometry(QtCore.QRect(x, y, progress_width, height))
        if self._current_value < self._aim_value:
            self.label.setStyleSheet("border: none;\n"
                                     "background-color: rgba(255, 255, 255, 0);\n"
                                     "color: white;")
        self.label.setText(f"{str(self._current_value)}/{str(self._aim_value)}")
