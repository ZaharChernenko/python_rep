from PyQt5 import QtGui
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QPushButton,
                             QSizePolicy, QVBoxLayout)

from setupUi import setupRegularFont


class Meal(QFrame):

    def __init__(self, parent, time, name, weight, calories, protein, fat, carb):
        super().__init__(parent)

        self.name = name
        self.weight = weight
        self.calories = calories
        self.protein = protein
        self.fat = fat
        self.carb = carb

        font = setupRegularFont(20)

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(545, 101))
        self.setStyleSheet("border-radius: 8px;\n"
                           "background-color: rgb(47, 47, 47);")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        self.main_horizontal_layout = QHBoxLayout(self)
        self.main_horizontal_layout.setContentsMargins(10, 5, 5, 5)
        self.main_horizontal_layout.setSpacing(10)

        self.time_label = QLabel(parent)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time_label.sizePolicy().hasHeightForWidth())
        self.time_label.setSizePolicy(sizePolicy)
        self.time_label.setMinimumSize(QSize(78, 0))
        self.time_label.setMaximumSize(QSize(78, 32))
        self.time_label.setFont(font)
        self.time_label.setStyleSheet("color: white;\n")
        self.time_label.setText(time)
        self.main_horizontal_layout.addWidget(self.time_label)

        self.dict_values_frame = QFrame(parent)
        self.dict_values_frame.setFrameShape(QFrame.StyledPanel)
        self.dict_values_frame.setFrameShadow(QFrame.Raised)

        self.dict_values_vertical_layout = QVBoxLayout(self.dict_values_frame)
        self.dict_values_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.dict_values_vertical_layout.setSpacing(0)

        self.name_frame = QFrame(self.dict_values_frame)
        self.name_frame.setFrameShape(QFrame.StyledPanel)
        self.name_frame.setFrameShadow(QFrame.Raised)

        self.name_label = QLabel(self.name_frame)
        self.name_label.setGeometry(QRect(0, 0, 438, 28))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name_label.sizePolicy().hasHeightForWidth())
        self.name_label.setSizePolicy(sizePolicy)
        font.setPointSize(18)
        self.name_label.setFont(font)
        self.name_label.setStyleSheet("color: white;")
        self.name_label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        if len(self.name) > 33:
            self.name_label.setText(self.name[:33])
        else:
            self.name_label.setText(self.name)

        self.delete_food_btn = QPushButton(self.name_frame)
        self.delete_food_btn.setGeometry(QRect(408, 0, 31, 30))
        self.delete_food_btn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.delete_food_btn.setStyleSheet("border: none;\n"
                                           "background-color: rgba(255, 255, 255, 0);")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("img/trash-icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_food_btn.setIcon(icon4)
        self.delete_food_btn.setIconSize(QSize(30, 30))

        self.dict_values_vertical_layout.addWidget(self.name_frame)

        self.weight_and_calories_frame = QFrame(self.dict_values_frame)
        self.weight_and_calories_frame.setFrameShape(QFrame.StyledPanel)
        self.weight_and_calories_frame.setFrameShadow(QFrame.Raised)

        self.weight_and_calories_layout = QHBoxLayout(self.weight_and_calories_frame)
        self.weight_and_calories_layout.setContentsMargins(0, 0, 0, 0)

        self.weight_label = QLabel(self.weight_and_calories_frame)
        self.weight_label.setMinimumSize(QSize(81, 0))
        self.weight_label.setMaximumSize(QSize(130, 16777215))
        font.setPointSize(16)
        self.weight_label.setFont(font)
        self.weight_label.setStyleSheet("color: white;")
        self.weight_label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.weight_label.setText(f"Вес: {str(self.weight)}")
        self.weight_and_calories_layout.addWidget(self.weight_label)

        self.calories_label = QLabel(self.weight_and_calories_frame)
        self.calories_label.setMinimumSize(QSize(60, 0))
        self.calories_label.setFont(font)
        self.calories_label.setStyleSheet("color: #B5A837;")
        self.calories_label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.calories_label.setText(f"Калории: {str(self.calories)}")
        self.weight_and_calories_layout.addWidget(self.calories_label)

        self.dict_values_vertical_layout.addWidget(self.weight_and_calories_frame)

        self.nutrients_frame = QFrame(self.dict_values_frame)
        self.nutrients_frame.setFrameShape(QFrame.StyledPanel)
        self.nutrients_frame.setFrameShadow(QFrame.Raised)

        self.nutrients_layout = QHBoxLayout(self.nutrients_frame)
        self.nutrients_layout.setContentsMargins(0, 0, 0, 0)

        self.protein_label = QLabel(self.nutrients_frame)
        self.protein_label.setMinimumSize(QSize(81, 0))
        self.protein_label.setMaximumSize(QSize(130, 16777215))
        self.protein_label.setFont(font)
        self.protein_label.setStyleSheet("color: #62D9C7;")
        self.protein_label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.protein_label.setText(f"Белки: {str(self.protein)}")
        self.nutrients_layout.addWidget(self.protein_label)

        self.fat_label = QLabel(self.nutrients_frame)
        self.fat_label.setMinimumSize(QSize(81, 0))
        self.fat_label.setMaximumSize(QSize(130, 16777215))
        self.fat_label.setFont(font)
        self.fat_label.setStyleSheet("color: #F59705;")
        self.fat_label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.fat_label.setText(f"Жиры: {str(self.fat)}")

        self.nutrients_layout.addWidget(self.fat_label)

        self.carb_label = QLabel(self.nutrients_frame)
        self.carb_label.setMinimumSize(QSize(81, 0))
        self.carb_label.setFont(font)
        self.carb_label.setStyleSheet("color: #D762D9;")
        self.carb_label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.carb_label.setText(f"Углеводы: {str(self.carb)}")
        self.nutrients_layout.addWidget(self.carb_label)

        self.dict_values_vertical_layout.addWidget(self.nutrients_frame)
        self.main_horizontal_layout.addWidget(self.dict_values_frame)
