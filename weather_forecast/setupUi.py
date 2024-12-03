from PyQt5.QtWidgets import QPushButton, QSizePolicy, QGraphicsColorizeEffect, QCompleter
from PyQt5.QtCore import QSize, Qt, QPropertyAnimation, QEvent, QEasingCurve
from PyQt5.QtGui import QFont, QCursor, QIcon, QPixmap, QColor


def setupRegularFont(font_size):
    regular_font = QFont()
    regular_font.setPointSize(font_size)
    return regular_font


def setupQCompleter(arr):
    completer = QCompleter(arr)
    completer.setCaseSensitivity(Qt.CaseInsensitive)
    completer.popup().setObjectName("completerPopup")
    completer.setMaxVisibleItems(15)
    completer.popup().setStyleSheet("color: white; background: rgba(96, 96, 96, 160); border-radius: 5px; font-size: "
                                    "14px;")
    return completer


class CustomButton(QPushButton):
    def __init__(self, parent, btn_width, btn_length, icon_width, icon_length, icon_name):
        super().__init__(parent)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(btn_width, btn_length))
        self.setMaximumSize(QSize(btn_width, btn_length))
        self.setCursor(QCursor(Qt.PointingHandCursor))

        icon = QIcon()
        icon.addPixmap(QPixmap(f"icons/{icon_name}"), QIcon.Normal, QIcon.Off)
        self.setIcon(icon)
        self.setIconSize(QSize(icon_width, icon_length))

        self.color_effect = QGraphicsColorizeEffect()
        self.color_effect.setColor(QColor(255, 255, 255, 128))
        self.setGraphicsEffect(self.color_effect)

        self.icon_anim = QPropertyAnimation(self.color_effect, b"color")
        self.icon_anim.setStartValue(QColor(255, 255, 255, 128))
        self.icon_anim.setEndValue(QColor(255, 255, 255, 255))
        self.icon_anim.setDuration(450)
        self.icon_anim.setEasingCurve(QEasingCurve.InQuad)

    def enterEvent(self, a0: QEvent):
        self.icon_anim.setDirection(self.icon_anim.Forward)
        self.icon_anim.start()

    def leaveEvent(self, a0: QEvent):
        self.icon_anim.setDirection(self.icon_anim.Backward)
        self.icon_anim.start()
