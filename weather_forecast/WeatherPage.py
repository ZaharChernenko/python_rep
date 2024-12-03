import datetime
import gettext
import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem, QLineEdit,
                             QLabel, QFrame, QScrollArea)
from PyQt5.QtCore import QSize, Qt, QRect, QTimer
from PyQt5.QtGui import QPixmap
from setupUi import setupRegularFont, CustomButton
from weatherTools import getWeatherData
from WeatherStructs import FullWeatherData, DailyWeatherDataElem


class WeatherPage(QWidget):
    def __init__(self, city_name: str, country_name: str, city_lat: float, city_lon: float,
                 weather_data: FullWeatherData, local_time_offset: int, completer,
                 is_added: bool, is_local_city: bool = False):
        super().__init__()

        self._is_added = is_added
        self._is_local_city = is_local_city

        self._city_name = city_name
        self._country_name = country_name
        self._city_lat = city_lat
        self._city_lon = city_lon
        self._current_city_time_offset = weather_data.timezone_offset

        self._cur_temp = weather_data.cur_temp
        self._max_temp = weather_data.max_temp
        self._min_temp = weather_data.min_temp
        self._icon_name = weather_data.icon
        self._local_time_offset = local_time_offset

        self.main_vlayout = QVBoxLayout(self)
        self.main_vlayout.setContentsMargins(0, 0, 0, 0)
        self.main_vlayout.setSpacing(0)

        self.upper_page_widget = QWidget(self)
        self.upper_page_widget.setMinimumSize(QSize(0, 65))
        self.upper_page_widget.setMaximumSize(QSize(16777215, 65))

        self.upper_page_hlayout = QHBoxLayout(self.upper_page_widget)
        self.upper_page_hlayout.setContentsMargins(15, 0, 20, 0)
        self.upper_page_hlayout.setSpacing(10)

        self.slider_btn = CustomButton(self.upper_page_widget, 50, 50, 45, 45,
                                       "slider_icon.svg")
        self.upper_page_hlayout.addWidget(self.slider_btn, 0, Qt.AlignBottom)

        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.upper_page_hlayout.addItem(spacerItem1)

        if not self._is_added:
            if sys.platform == "darwin":
                self.add_btn = CustomButton(self.upper_page_widget, 23, 23, 23, 23,
                                            "add_icon.svg")
            else:
                self.add_btn = CustomButton(self.upper_page_widget, 27, 27, 27, 27,
                                            "add_icon.svg")
            self.add_btn.setStyleSheet("border: 2px solid #7f7f7f; border-radius: 3px")
            self.upper_page_hlayout.addWidget(self.add_btn)
        else:
            if not self._is_local_city:
                if sys.platform == "darwin":
                    self.delete_btn = CustomButton(self.upper_page_widget, 23, 23, 23, 23,
                                                   "delete_icon.svg")
                else:
                    self.delete_btn = CustomButton(self.upper_page_widget, 27, 27, 27, 27,
                                                   "delete_icon.svg")
                self.delete_btn.setStyleSheet("border: 2px solid #7f7f7f; border-radius: 3px")
                self.upper_page_hlayout.addWidget(self.delete_btn)

        self.weather_line_edit = QLineEdit(self.upper_page_widget)
        self.weather_line_edit.setMinimumSize(QSize(250, 0))
        self.weather_line_edit.setMaximumSize(QSize(350, 16777215))
        font = setupRegularFont(14)
        self.weather_line_edit.setFont(font)
        self.weather_line_edit.setStyleSheet("border: 1px solid white; border-radius: 3px; padding-left:3px;")
        self.weather_line_edit.setPlaceholderText("Поиск:")
        self.completer = completer
        self.weather_line_edit.setCompleter(self.completer)
        self.upper_page_hlayout.addWidget(self.weather_line_edit)
        self.main_vlayout.addWidget(self.upper_page_widget)

        self.main_page_widget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.main_page_widget.setSizePolicy(sizePolicy)

        self.main_page_vlayout = QVBoxLayout(self.main_page_widget)
        self.main_page_vlayout.setContentsMargins(45, 0, 45, 0)
        self.main_page_vlayout.setSpacing(0)

        self.city_label = QLabel(self.main_page_widget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.city_label.setSizePolicy(sizePolicy)
        self.city_label.setMinimumSize(QSize(0, 38))
        self.city_label.setMaximumSize(QSize(16777215, 38))
        font.setPointSize(25)
        self.city_label.setFont(font)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.main_page_vlayout.addWidget(self.city_label)

        self.temp_label = QLabel(self.main_page_widget)
        self.temp_label.setMaximumSize(QSize(16777215, 44))
        font.setPointSize(38)
        self.temp_label.setFont(font)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.main_page_vlayout.addWidget(self.temp_label)

        self.weather_label = QLabel(self.main_page_widget)
        self.weather_label.setMinimumSize(QSize(0, 23))
        self.weather_label.setMaximumSize(QSize(16777215, 23))
        font.setPointSize(11)
        self.weather_label.setFont(font)
        self.weather_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.main_page_vlayout.addWidget(self.weather_label)

        self.max_min_temp_label = QLabel(self.main_page_widget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.max_min_temp_label.setSizePolicy(sizePolicy)
        self.max_min_temp_label.setMinimumSize(QSize(0, 18))
        self.max_min_temp_label.setMaximumSize(QSize(16777215, 18))
        font.setPointSize(11)
        self.max_min_temp_label.setFont(font)
        self.max_min_temp_label.setAlignment(Qt.AlignCenter)
        self.main_page_vlayout.addWidget(self.max_min_temp_label)
        spacerItem2 = QSpacerItem(20, 25, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.main_page_vlayout.addItem(spacerItem2)

        self.main_page_scroll_area = QScrollArea(self.main_page_widget)
        self.main_page_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.main_page_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.main_page_scroll_area.setWidgetResizable(True)

        self.main_page_scroll_widget = QWidget()
        self.main_page_scroll_widget.setGeometry(QRect(0, 0, 560, 1245))

        self.main_page_scroll_vlayout = QVBoxLayout(self.main_page_scroll_widget)
        self.main_page_scroll_vlayout.setContentsMargins(0, 0, 0, 0)
        self.main_page_scroll_vlayout.setSpacing(15)

        self.hourly_widget = QWidget(self.main_page_scroll_widget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hourly_widget.sizePolicy().hasHeightForWidth())
        self.hourly_widget.setSizePolicy(sizePolicy)
        self.hourly_widget.setMinimumSize(QSize(0, 145))
        self.hourly_widget.setMaximumSize(QSize(16777215, 145))
        self.hourly_widget.setObjectName("hourly_widget")
        self.hourly_widget.setStyleSheet("#hourly_widget{\n"
                                         "    background: rgba(96, 96, 96, 128);\n"
                                         "    border-radius: 10px;\n"
                                         "}")

        self.hourly_vlayout = QVBoxLayout(self.hourly_widget)
        self.hourly_vlayout.setContentsMargins(6, 0, 0, 0)

        self.hourly_frame = QFrame(self.hourly_widget)
        self.hourly_frame.setMinimumSize(QSize(0, 30))
        self.hourly_frame.setMaximumSize(QSize(16777215, 30))
        self.hourly_frame.setObjectName("hourly_frame")
        self.hourly_frame.setStyleSheet("#hourly_frame{\n"
                                        "    border-bottom: 1px solid #d5d6d7;\n"
                                        "}")
        self.hourly_frame.setFrameShape(QFrame.StyledPanel)
        self.hourly_frame.setFrameShadow(QFrame.Raised)

        self.hourly_frame_hlayout = QHBoxLayout(self.hourly_frame)
        self.hourly_frame_hlayout.setContentsMargins(0, 0, 0, 0)
        self.hourly_frame_hlayout.setSpacing(7)

        self.hourly_icon_label = QLabel(self.hourly_frame)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hourly_icon_label.sizePolicy().hasHeightForWidth())
        self.hourly_icon_label.setSizePolicy(sizePolicy)
        self.hourly_icon_label.setMinimumSize(QSize(15, 15))
        self.hourly_icon_label.setMaximumSize(QSize(15, 15))
        self.hourly_icon_label.setPixmap(QPixmap("icons/hour_icon.svg"))
        self.hourly_icon_label.setScaledContents(True)
        self.hourly_frame_hlayout.addWidget(self.hourly_icon_label)

        self.hourly_label = QLabel(self.hourly_frame)
        font.setPointSize(11)
        self.hourly_label.setFont(font)
        self.hourly_label.setStyleSheet("color: #d5d6d7;")
        self.hourly_frame_hlayout.addWidget(self.hourly_label)
        self.hourly_vlayout.addWidget(self.hourly_frame)

        self.main_vlayout.addWidget(self.main_page_widget)

        self.hourly_scroll_area = QScrollArea(self.hourly_widget)
        self.hourly_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.hourly_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.hourly_scroll_area.setWidgetResizable(True)

        self.hourly_scroll_area_widget = QWidget()
        self.hourly_scroll_area_widget.setGeometry(QRect(0, 0, 480, 109))

        self.hourly_scroll_area_hlayout = QHBoxLayout(self.hourly_scroll_area_widget)
        self.hourly_scroll_area_hlayout.setContentsMargins(0, 0, 0, -1)
        self.hourly_scroll_area_hlayout.setSpacing(2)

        self.hourly_scroll_area.setWidget(self.hourly_scroll_area_widget)
        self.hourly_vlayout.addWidget(self.hourly_scroll_area)
        self.main_page_scroll_vlayout.addWidget(self.hourly_widget)

        self.daily_widget = QWidget(self.main_page_scroll_widget)
        self.daily_widget.setMinimumSize(QSize(350, 358))
        self.daily_widget.setMaximumSize(QSize(16777215, 16777215))
        self.daily_widget.setStyleSheet("#daily_widget{\n"
                                        "    background: rgba(96, 96, 96, 128);\n"
                                        "    border-radius: 10px;\n"
                                        "}")
        self.daily_widget.setObjectName("daily_widget")

        self.daily_vlayout = QVBoxLayout(self.daily_widget)
        self.daily_vlayout.setContentsMargins(6, 0, 0, 0)
        self.daily_vlayout.setSpacing(0)
        self.daily_vlayout.setObjectName("daily_vlayout")
        self.daily_frame = QFrame(self.daily_widget)
        self.daily_frame.setMinimumSize(QSize(0, 30))
        self.daily_frame.setMaximumSize(QSize(16777215, 30))
        self.daily_frame.setFrameShape(QFrame.StyledPanel)
        self.daily_frame.setFrameShadow(QFrame.Raised)
        self.daily_frame.setObjectName("daily_frame")

        self.daily_frame_hlayout = QHBoxLayout(self.daily_frame)
        self.daily_frame_hlayout.setContentsMargins(0, 0, 0, 0)
        self.daily_frame_hlayout.setSpacing(7)
        self.daily_frame_hlayout.setObjectName("daily_frame_hlayout")
        self.label = QLabel(self.daily_frame)
        self.label.setMinimumSize(QSize(15, 16))
        self.label.setMaximumSize(QSize(15, 16))
        self.label.setText("")
        self.label.setPixmap(QPixmap("icons/calendar_icon.svg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.daily_frame_hlayout.addWidget(self.label)

        self.label_2 = QLabel(self.daily_frame)
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: #d5d6d7;")
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Прогноз на 8 дней:")
        self.daily_frame_hlayout.addWidget(self.label_2)
        self.daily_vlayout.addWidget(self.daily_frame)
        self.daily_main_frame = QFrame(self.daily_widget)
        self.daily_main_frame.setFrameShape(QFrame.StyledPanel)
        self.daily_main_frame.setFrameShadow(QFrame.Raised)
        self.daily_main_frame.setObjectName("daily_main_frame")

        self.daily_main_frame_vlayout = QVBoxLayout(self.daily_main_frame)
        self.daily_main_frame_vlayout.setContentsMargins(0, 0, 0, 0)
        self.daily_main_frame_vlayout.setSpacing(0)
        self.daily_main_frame_vlayout.setObjectName("daily_main_frame_vlayout")

        self.daily_vlayout.addWidget(self.daily_main_frame)

        self.main_page_scroll_vlayout.addWidget(self.daily_widget)
        spacerItem3 = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self.main_page_scroll_vlayout.addItem(spacerItem3)
        self.main_page_scroll_area.setWidget(self.main_page_scroll_widget)
        self.main_page_vlayout.addWidget(self.main_page_scroll_area)
        self.main_vlayout.addWidget(self.main_page_widget)

        self.city_label.setText(self._city_name)
        self.temp_label.setText(f"{self._cur_temp}°")
        self.weather_label.setText(weather_data.cur_weather)
        self.max_min_temp_label.setText(f"Макс: {self._max_temp}°, мин: {self._min_temp}°")
        self.hourly_label.setText("Прогноз на 48 часов:")
        self.createHourlyAndDailyWidgets(weather_data.hourly, weather_data.daily)

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.refreshData(getWeatherData(self._city_lat, self._city_lon)))
        self.timer.start(300000)

    def deleteLater(self):
        super().deleteLater()
        self.timer.deleteLater()  # python does not delete timer automatically and will try to call refreshData

    def createHourlyAndDailyWidgets(self, hourly, daily):
        self.list_of_hourly_elements = []
        for hour in hourly:
            hourly_element = HourlyElement(self.hourly_scroll_area_widget, hour.dt,
                                           hour.icon, hour.temp,
                                           self._current_city_time_offset,
                                           self._local_time_offset)
            self.hourly_scroll_area_hlayout.addWidget(hourly_element)
            self.list_of_hourly_elements.append(hourly_element)
        self.list_of_daily_elements = []
        for day in daily:
            daily_element = DailyElement(parent=self.daily_main_frame,
                                         day_data=day,
                                         current_city_time_offset=self._current_city_time_offset,
                                         local_time_offset=self._local_time_offset)
            self.daily_main_frame_vlayout.addWidget(daily_element)
            self.list_of_daily_elements.append(daily_element)

    def getAdd(self):
        return self._is_added

    def setAdd(self, is_added: bool):
        self._is_added = is_added

    def getIsLocalCity(self):
        return self._is_local_city

    def getCity(self):
        return self._city_name

    def getCountry(self):
        return self._country_name

    def getIconName(self):
        return self._icon_name

    def getCityDict(self) -> dict:
        """Returns all necessary data for user_data.json"""
        return {"name": self._city_name, "country": self._country_name,
                "coord": {"lat": self._city_lat, "lon": self._city_lon}}

    def getDataToWeatherFrame(self) -> tuple:
        return (self._city_name, self._cur_temp, self._max_temp, self._min_temp,
                self._icon_name, self._current_city_time_offset)

    def changeAddBtnToDeleteBtn(self):
        self.add_btn.deleteLater()
        if sys.platform == "darwin":
            self.delete_btn = CustomButton(self.upper_page_widget, 23, 23, 23, 23,
                                           "delete_icon.svg")
        else:
            self.delete_btn = CustomButton(self.upper_page_widget, 27, 27, 27, 27,
                                           "delete_icon.svg")
        self.delete_btn.setStyleSheet("border: 2px solid; border-radius: 3px")
        self.upper_page_hlayout.insertWidget(2, self.delete_btn)

    def refreshData(self, weather_data: FullWeatherData):
        self._cur_temp = weather_data.cur_temp
        self._max_temp = weather_data.max_temp
        self._min_temp = weather_data.min_temp
        self._icon_name = weather_data.icon

        self.temp_label.setText(f"{self._cur_temp}°")
        self.weather_label.setText(weather_data.cur_weather)
        self.max_min_temp_label.setText(f"Макс: {self._max_temp}°, мин: {self._min_temp}°")
        for hourly_element in self.list_of_hourly_elements:
            hourly_element.deleteLater()
        for daily_element in self.list_of_daily_elements:
            daily_element.deleteLater()
        self.createHourlyAndDailyWidgets(weather_data.hourly, weather_data.daily)


class HourlyElement(QFrame):
    def __init__(self, parent, time: int, icon: str, temp: int, current_city_time_offset: int, local_time_offset: int):
        super().__init__(parent)

        self.setMinimumSize(QSize(58, 80))
        self.setMaximumSize(QSize(58, 80))
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)

        font = setupRegularFont(11)

        self.hourly_time_label = QLabel(self)
        self.hourly_time_label.setFont(font)
        self.hourly_time_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.hourly_time_label)
        self.hourly_weather_label = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hourly_weather_label.sizePolicy().hasHeightForWidth())
        self.hourly_weather_label.setSizePolicy(sizePolicy)
        self.hourly_weather_label.setMinimumSize(QSize(40, 40))
        self.hourly_weather_label.setMaximumSize(QSize(40, 40))
        font.setPointSize(11)
        self.hourly_weather_label.setFont(font)
        self.hourly_weather_label.setText("")
        self.hourly_weather_label.setPixmap(QPixmap(f"icons/{icon}.png"))
        self.hourly_weather_label.setScaledContents(True)
        self.hourly_weather_label.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.hourly_weather_label, 0, Qt.AlignHCenter)

        self.hourly_temp_label = QLabel(self)
        font.setPointSize(14)
        self.hourly_temp_label.setFont(font)
        self.hourly_temp_label.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.hourly_temp_label)

        self.hourly_temp_label.setText(f"{temp}°")
        self.time = time + current_city_time_offset - local_time_offset
        self.hourly_time_label.setText(datetime.datetime.fromtimestamp(self.time).strftime("%H"))


class DailyElement(QFrame):
    def __init__(self, parent, day_data: DailyWeatherDataElem, current_city_time_offset: int, local_time_offset: int):
        super().__init__(parent)

        days_translator = gettext.translation('days_translate', './locale', languages=['ru'])
        days_translator.install()

        self.setMinimumSize(QSize(0, 40))
        self.setMaximumSize(QSize(16777215, 40))
        self.setObjectName("daily_element")
        self.setStyleSheet("#daily_element{\n"
                           "    border-top: 1px solid #d5d6d7;\n"
                           "}")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(9, 0, 0, 0)
        self.horizontalLayout.setSpacing(10)

        font = setupRegularFont(14)

        self.daily_date_label = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.daily_date_label.sizePolicy().hasHeightForWidth())
        self.daily_date_label.setSizePolicy(sizePolicy)
        self.daily_date_label.setMinimumSize(QSize(25, 0))
        self.daily_date_label.setMaximumSize(QSize(25, 16777215))
        self.daily_date_label.setFont(font)
        self.day = day_data.dt + current_city_time_offset - local_time_offset
        self.daily_date_label.setText(_(datetime.datetime.fromtimestamp(self.day).strftime("%a")))
        self.horizontalLayout.addWidget(self.daily_date_label)

        self.weather_label = QLabel(self)
        self.weather_label.setMinimumSize(QSize(40, 40))
        self.weather_label.setMaximumSize(QSize(40, 40))
        self.weather_label.setPixmap(QPixmap(f"icons/{day_data.icon}"))
        self.weather_label.setScaledContents(True)
        self.horizontalLayout.addWidget(self.weather_label)

        self.temp_label = QLabel(self)
        font.setPointSize(13)
        self.temp_label.setFont(font)
        self.temp_label.setText(f"Средняя: {day_data.average_temp}° \
        | Мин: {day_data.min_temp}° | Макс: {day_data.max_temp}°")
        self.horizontalLayout.addWidget(self.temp_label)
