from PyQt5.QtWidgets import QFrame, QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import QSize, Qt, QPropertyAnimation, pyqtProperty, QTime
from PyQt5.QtGui import QCursor, QIcon, QPixmap, QColor, QPalette
from setupUi import setupRegularFont


class WeatherFrame(QFrame):
    def __init__(self, parent, city_name: str, temp: int, max_temp: int, min_temp: int, icon_name: str,
                 current_city_time_offset: int, local_time_offset: int):
        super().__init__(parent)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(205, 79))
        self.setMaximumSize(QSize(205, 79))

        regular_font = setupRegularFont(14)
        self.setFont(regular_font)
        self.setObjectName("button_frame")
        self.setStyleSheet("#button_frame{border-bottom: 1px solid rgba(255, 255, 255, 0.5);}")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        self.main_vlayout = QVBoxLayout(self)
        self.main_vlayout.setContentsMargins(7, 0, 7, 0)
        self.main_vlayout.setSpacing(0)

        self.main_btn_frame = QFrame(self)
        self.main_btn_frame.setFrameShape(QFrame.StyledPanel)
        self.main_btn_frame.setFrameShadow(QFrame.Raised)

        self.main_btn_frame_hlayout = QHBoxLayout(self.main_btn_frame)
        self.main_btn_frame_hlayout.setContentsMargins(0, 0, 0, 0)
        self.main_btn_frame_hlayout.setSpacing(0)

        self.city_time_frame = QFrame(self.main_btn_frame)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.city_time_frame.sizePolicy().hasHeightForWidth())
        self.city_time_frame.setSizePolicy(sizePolicy)
        self.city_time_frame.setMinimumSize(QSize(0, 44))
        self.city_time_frame.setFrameShape(QFrame.StyledPanel)
        self.city_time_frame.setFrameShadow(QFrame.Raised)

        self.city_time_vlayout = QVBoxLayout(self.city_time_frame)
        self.city_time_vlayout.setContentsMargins(0, 0, 0, 0)
        self.city_time_vlayout.setSpacing(0)

        self.city_btn = QPushButton(self.city_time_frame)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.city_btn.sizePolicy().hasHeightForWidth())
        self.city_btn.setSizePolicy(sizePolicy)
        self.city_btn.setMinimumSize(QSize(146, 30))
        self.city_btn.setMaximumSize(QSize(146, 30))
        self.city_btn.setFont(regular_font)
        self.city_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.city_btn.setStyleSheet("text-align: left;")
        self.city_btn.setAutoDefault(False)
        self.city_btn.setDefault(False)
        self.city_btn.setFlat(False)
        self.city_time_vlayout.addWidget(self.city_btn)

        self.time_btn = QPushButton(self.city_time_frame)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time_btn.sizePolicy().hasHeightForWidth())
        self.time_btn.setSizePolicy(sizePolicy)
        self.time_btn.setMinimumSize(QSize(146, 14))
        self.time_btn.setMaximumSize(QSize(146, 14))
        regular_font.setPointSize(9)
        self.time_btn.setFont(regular_font)
        self.time_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.time_btn.setStyleSheet("text-align: left;")
        self.city_time_vlayout.addWidget(self.time_btn)
        self.main_btn_frame_hlayout.addWidget(self.city_time_frame)

        self.temp_btn = QPushButton(self.main_btn_frame)
        self.temp_btn.setMinimumSize(QSize(0, 51))
        self.temp_btn.setMaximumSize(QSize(16777215, 51))
        regular_font.setPointSize(26)
        self.temp_btn.setFont(regular_font)
        self.temp_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.main_btn_frame_hlayout.addWidget(self.temp_btn, 0, Qt.AlignRight)

        self.main_vlayout.addWidget(self.main_btn_frame)

        self.weather_btn = QPushButton(self)
        self.weather_btn.setMinimumSize(QSize(0, 35))
        self.weather_btn.setMaximumSize(QSize(16777215, 35))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.weather_btn.sizePolicy().hasHeightForWidth())
        self.weather_btn.setSizePolicy(sizePolicy)
        regular_font.setPointSize(11)
        self.weather_btn.setFont(regular_font)
        self.weather_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.weather_btn.setStyleSheet("text-align: right;")
        icon = QIcon()
        icon.addPixmap(QPixmap(f"icons/{icon_name}.png"), QIcon.Normal, QIcon.Off)
        self.weather_btn.setIcon(icon)
        self.weather_btn.setIconSize(QSize(36, 36))
        self.main_vlayout.addWidget(self.weather_btn)

        self.current_city_time_offset = current_city_time_offset
        self.local_time_offset = local_time_offset

        self.city_btn.setText(city_name)
        self.temp_btn.setText(f"{temp}°")
        self.weather_btn.setText(f"Макс: {max_temp}° | Мин: {min_temp}°")
        self.setTime(QTime().currentTime())

        self.current_background_color = QPalette.Window
        self.background_anim = QPropertyAnimation(self, b"background")
        self.background_anim.setStartValue(QColor(96, 96, 96, 0))
        self.background_anim.setEndValue(QColor(96, 96, 96, 128))
        self.background_anim.setDuration(300)

    def deleteLater(self):
        super().deleteLater()
        self.city_btn.deleteLater()
        self.temp_btn.deleteLater()
        self.time_btn.deleteLater()
        self.weather_btn.deleteLater()

    def parseStyleSheet(self):
        style_sheet_string = self.styleSheet()
        style_sheet_list = [s.strip() for s in style_sheet_string.split(';')]
        return style_sheet_list

    def getBackgroundColor(self):
        return self.palette().color(self.current_background_color)

    def setBackgroundColor(self, color):
        stylesheet_list = self.parseStyleSheet()
        bg_new = 'background-color: rgba(%d,%d,%d,%d)' % (color.red(), color.green(), color.blue(), color.alpha())

        for i, string in enumerate(stylesheet_list):
            if 'background-color' in string:
                stylesheet_list[i] = bg_new
                break
        else:
            stylesheet_list.insert(-1, bg_new)

        self.setStyleSheet('; '.join(stylesheet_list))

    background = pyqtProperty(QColor, getBackgroundColor, setBackgroundColor)

    def removeBorder(self):
        style_sheet_list = self.parseStyleSheet()
        for i, string in enumerate(style_sheet_list):
            if "border-bottom" in string:
                style_sheet_list[i] = "#button_frame{border-radius: 10px;"
        self.setStyleSheet('; '.join(style_sheet_list))

    def addBorder(self):
        self.setStyleSheet("#button_frame{border-bottom: 1px solid rgba(255, 255, 255, 0.5);}")

    def animActiveBtn(self):
        self.background_anim.start()
        self.removeBorder()

    def setFrameActive(self, is_active: bool):
        if is_active:
            self.animActiveBtn()
            self.temp_btn.setDisabled(True)
            self.city_btn.setDisabled(True)
            self.time_btn.setDisabled(True)
            self.weather_btn.setDisabled(True)
        else:
            self.addBorder()
            self.temp_btn.setEnabled(True)
            self.city_btn.setEnabled(True)
            self.time_btn.setEnabled(True)
            self.weather_btn.setEnabled(True)

    def setTime(self, time):
        current_time = time
        current_time = current_time.addSecs(self.current_city_time_offset - self.local_time_offset)
        self.time_btn.setText(current_time.toString("hh:mm"))

    def refreshData(self, temp: int, max_temp: int, min_temp: int, icon_name: str):
        self.temp_btn.setText(f"{temp}°")
        self.weather_btn.setText(f"Макс: {max_temp}° | Мин: {min_temp}°")
        icon = QIcon()
        icon.addPixmap(QPixmap(f"icons/{icon_name}.png"), QIcon.Normal, QIcon.Off)
        self.weather_btn.setIcon(icon)
