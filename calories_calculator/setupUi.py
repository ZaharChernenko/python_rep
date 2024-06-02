from sys import platform

from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import QCursor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QPushButton, QSizePolicy


def setupRegularFont(font_size):
    font = QFont()
    font.setFamily("TT Norms Pro")
    font.setPointSize(font_size)
    return font


def setupMediumFont(font_size):
    medium_font = QFont()
    if platform == "win32":
        medium_font.setFamily("TT Norms Pro Medium")
        medium_font.setPointSize(font_size - 3)
    else:
        medium_font.setFamily("TT Norms Pro")
        medium_font.setWeight(500)
        medium_font.setPointSize(font_size)
    return medium_font


def setupHeader(parent):
    header = QLabel(parent)
    header.setGeometry(QRect(0, 0, 600, 90))
    sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(header.sizePolicy().hasHeightForWidth())
    header.setSizePolicy(sizePolicy)
    header.setStyleSheet("padding-left: 100px;\n"
                         "border-bottom: 1px solid black;\n"
                         "background-color: rgb(47, 47, 47);\n"
                         "color: rgb(255, 255, 255);\n"
                         "")
    header.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
    header.setWordWrap(False)
    return header


def setupBurgerBtn(parent):
    burger_btn = QPushButton(parent)
    burger_btn.setGeometry(QRect(20, 20, 48, 48))
    burger_btn.setCursor(QCursor(Qt.PointingHandCursor))
    burger_btn.setStyleSheet("border: none;\n"
                             "background-color: rgba(255, 255, 255, 0);")
    icon = QIcon()
    icon.addPixmap(QPixmap("img/burger-icon.png"), QIcon.Normal, QIcon.On)
    burger_btn.setIcon(icon)
    burger_btn.setIconSize(QSize(48, 48))
    burger_btn.setAutoDefault(False)
    burger_btn.setObjectName("burger_btn")
    return burger_btn
