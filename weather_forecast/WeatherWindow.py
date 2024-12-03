import bisect
import time
import os
import re
from json import loads, dump
from setupUi import setupQCompleter
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QTimer, QTime
from WeatherStructs import FullWeatherData
from WeatherPage import WeatherPage
from WeatherFrame import WeatherFrame
from weatherTools import _getCurrentLocation, getWeatherData
from filesTools import loadUserData, readCityDict
from exceptions import IpReceivingError


class WeatherWindow:
    def __init__(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(811, 670)
        main_window.setStyleSheet("*{\n"
                                  "    border: none;\n"
                                  "    background-color: transparent;\n"
                                  "    background: transparent;\n"
                                  "    padding: 0;\n"
                                  "    margin: 0;\n"
                                  "    color: #fff;\n"
                                  "}\n"
                                  "#central_widget{\n"
                                  "    background-color: #1f232a;\n"
                                  "    border-image: url(img/01d.jpg) 0 0 0 0 stretch stretch;\n"
                                  "}\n"
                                  "\n"
                                  "#slider{\n"
                                  "    margin: 20 0 20 0;\n"
                                  "    border-right: 1px solid rgba(255, 255, 255, 0.5);\n"
                                  "}\n"
                                  "\n"
                                  "#weather_line_edit{\n"
                                  "    border-radius: 3px;\n"
                                  "    padding-left: 2px;\n"
                                  "}"
                                  )

        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")

        self.main_hlayout = QtWidgets.QHBoxLayout(self.central_widget)
        self.main_hlayout.setContentsMargins(0, 0, 0, 0)
        self.main_hlayout.setSpacing(0)

        self.is_expanded = True
        self.slider = QtWidgets.QWidget(self.central_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.slider.sizePolicy().hasHeightForWidth())
        self.slider.setSizePolicy(sizePolicy)
        self.slider.setMinimumSize(QtCore.QSize(235, 0))
        self.slider.setMaximumSize(QtCore.QSize(235, 16777215))
        self.slider.setObjectName("slider")

        self.slider_vlayout = QtWidgets.QVBoxLayout(self.slider)
        self.slider_vlayout.setContentsMargins(0, 0, 0, 0)
        self.slider_vlayout.setSpacing(0)

        self.scroll_area = QtWidgets.QScrollArea(self.slider)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area_widget = QtWidgets.QWidget()
        self.scroll_area_widget.setGeometry(QtCore.QRect(0, 0, 235, 670))

        self.scroll_area_vlayout = QtWidgets.QVBoxLayout(self.scroll_area_widget)
        self.scroll_area_vlayout.setContentsMargins(15, 20, 0, 0)
        self.scroll_area_vlayout.setSpacing(0)

        self.local_timezone_offset = -time.timezone

        self.current_city_geo = None
        self.getCurrentLocation()

        self.current_city_data = getWeatherData(*self.current_city_geo.latlng)

        self.main_widget = QtWidgets.QWidget(self.central_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_widget.sizePolicy().hasHeightForWidth())
        self.main_widget.setSizePolicy(sizePolicy)
        self.main_widget.setObjectName("main_widget")
        self.main_widget_vlayout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_widget_vlayout.setContentsMargins(0, 0, 0, 0)
        self.main_widget_vlayout.setSpacing(0)
        self.main_widget_vlayout.setObjectName("main_widget_vlayout")

        self.stacked_widget = QtWidgets.QStackedWidget(self.main_widget)
        self.stacked_widget.setObjectName("stacked_widget")
        self.main_widget_vlayout.addWidget(self.stacked_widget)

        self.cities_dict = readCityDict()
        self.completer = setupQCompleter([f"{city_tuple.name}, {country}" for country in self.cities_dict
                                          for city_tuple in self.cities_dict[country]])

        self.current_city_page = WeatherPage(self.current_city_geo.city,
                                             "",
                                             *self.current_city_geo.latlng,
                                             weather_data=self.current_city_data,
                                             local_time_offset=self.local_timezone_offset,
                                             completer=self.completer,
                                             is_added=True, is_local_city=True)
        self.stacked_widget.addWidget(self.current_city_page)

        self.city_pages_list = [self.current_city_page]
        self.central_widget.setStyleSheet("#central_widget{border-image: url(img/" +
                                          self.current_city_page.getIconName() + ".jpg) 0 0 0 0 stretch stretch;}")

        self.current_city_frame = WeatherFrame(self.scroll_area_widget, "Текущее место",
                                               *(self.current_city_page.getDataToWeatherFrame()[1:]),
                                               local_time_offset=self.local_timezone_offset)

        self.current_city_frame.setFrameActive(True)
        self.scroll_area_vlayout.addWidget(self.current_city_frame)
        self.city_frames_list = [self.current_city_frame]

        self.scroll_area.setWidget(self.scroll_area_widget)
        self.slider_vlayout.addWidget(self.scroll_area)
        self.main_hlayout.addWidget(self.slider)

        self.main_hlayout.addWidget(self.main_widget)
        main_window.setCentralWidget(self.central_widget)
        main_window.setWindowTitle("Прогноз погоды")
        self.stacked_widget.setCurrentIndex(0)

        self.added_cities_list = []
        if os.path.isfile("./data/user_data.json"):
            user_data = loadUserData()
            if user_data:
                self.added_cities_list = loads(user_data)
                for city in self.added_cities_list:
                    self.createPage(city["name"], city["country"], city["coord"]["lat"], city["coord"]["lon"],
                                    getWeatherData(city["coord"]["lat"], city["coord"]["lon"]), True)
                    self.createWeatherFrame(self.city_pages_list[-1])

        self.spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                                QtWidgets.QSizePolicy.MinimumExpanding)
        self.scroll_area_vlayout.addItem(self.spacerItem)

        self.animation_compression_max = QtCore.QPropertyAnimation(self.slider, b"maximumWidth")
        self.animation_compression_max.setDuration(800)
        self.animation_compression_max.setStartValue(235)
        self.animation_compression_max.setEndValue(0)
        self.animation_compression_max.setEasingCurve(QtCore.QEasingCurve.OutQuart)

        self.animation_compression_min = QtCore.QPropertyAnimation(self.slider, b"minimumWidth")
        self.animation_compression_min.setDuration(800)
        self.animation_compression_min.setStartValue(235)
        self.animation_compression_min.setEndValue(0)
        self.animation_compression_min.setEasingCurve(QtCore.QEasingCurve.OutQuart)

        self.animation_expansion_max = QtCore.QPropertyAnimation(self.slider, b"maximumWidth")
        self.animation_expansion_max.setDuration(800)
        self.animation_expansion_max.setStartValue(0)
        self.animation_expansion_max.setEndValue(235)
        self.animation_expansion_max.setEasingCurve(QtCore.QEasingCurve.OutBack)

        self.animation_expansion_min = QtCore.QPropertyAnimation(self.slider, b"minimumWidth")
        self.animation_expansion_min.setDuration(800)
        self.animation_expansion_min.setStartValue(0)
        self.animation_expansion_min.setEndValue(235)
        self.animation_expansion_min.setEasingCurve(QtCore.QEasingCurve.OutBack)

        self.timer = QTimer()
        self.timer.timeout.connect(self.refreshFramesTime)
        self.timer.start(10000)

        self.icon_exp = re.compile(r"url\(img/\d{2}[d,n].jpg\)")

        self.current_city_frame.city_btn.clicked.connect(lambda: self.changePage(self.current_city_page))
        self.current_city_frame.temp_btn.clicked.connect(lambda: self.changePage(self.current_city_page))
        self.current_city_frame.time_btn.clicked.connect(lambda: self.changePage(self.current_city_page))
        self.current_city_frame.weather_btn.clicked.connect(lambda: self.changePage(self.current_city_page))
        self.current_city_page.timer.timeout.connect(lambda: self.current_city_frame.refreshData(
            *self.current_city_page.getDataToWeatherFrame()[1:5]))
        self.current_city_page.slider_btn.clicked.connect(self.sliderAnimation)

        self.completer.activated.connect(
            lambda: self.createPageFromSearch(
                self.city_pages_list[self.stacked_widget.currentIndex()].weather_line_edit.text()))

    def getCurrentLocation(self):
        try:
            self.current_city_geo = _getCurrentLocation()
        except IpReceivingError:
            self.createInternetWarningWindow()

    def sliderAnimation(self):
        if self.is_expanded:
            self.animation_compression_max.start()
            self.animation_compression_min.start()
            self.is_expanded = False

        else:
            self.animation_expansion_max.start()
            self.animation_expansion_min.start()
            self.is_expanded = True

    def setBackgroundImage(self, icon_name: str):
        self.central_widget.setStyleSheet(self.icon_exp.sub(f"url(img/{icon_name}.jpg)",
                                                            self.central_widget.styleSheet()))

    def changePage(self, page: WeatherPage, is_from_search: bool = False):
        self.setBackgroundImage(page.getIconName())
        prev_index = self.stacked_widget.currentIndex()
        if self.city_pages_list[prev_index].getAdd():
            self.city_frames_list[prev_index].setFrameActive(False)
            if prev_index > 0:
                self.city_frames_list[prev_index - 1].addBorder()
        else:
            self.stacked_widget.removeWidget(self.city_pages_list[prev_index])
            self.city_pages_list[prev_index].deleteLater()
            del self.city_pages_list[prev_index]

        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(page))
        cur_index = self.stacked_widget.currentIndex()

        if page.getAdd():
            self.city_frames_list[cur_index].setFrameActive(True)
            if cur_index > 0:
                self.city_frames_list[cur_index - 1].removeBorder()

        self.animation_page = QtCore.QPropertyAnimation(page, b"geometry")
        self.animation_page.setDuration(550)
        if cur_index < prev_index or is_from_search:
            self.animation_page.setStartValue(
                QtCore.QRect(0, -self.central_widget.height(), self.stacked_widget.width(),
                             self.stacked_widget.height()))

            self.animation_page.setEndValue(
                QtCore.QRect(0, 0, self.stacked_widget.width(), self.stacked_widget.height()))
        else:
            self.animation_page.setStartValue(
                QtCore.QRect(0, self.central_widget.height(), self.stacked_widget.width(),
                             self.stacked_widget.height()))

            self.animation_page.setEndValue(
                QtCore.QRect(0, 0, self.stacked_widget.width(), self.stacked_widget.height()))

        self.animation_page.setEasingCurve(QtCore.QEasingCurve.OutBack)
        self.animation_page.start()

    def createPage(self, city_name: str, country_name: str, lat: int, lon: int, weather_data: FullWeatherData,
                   is_added: bool):
        page = WeatherPage(city_name, country_name, lat, lon,
                           weather_data=weather_data,
                           local_time_offset=self.local_timezone_offset,
                           completer=self.completer,
                           is_added=is_added)
        self.city_pages_list.append(page)
        self.stacked_widget.addWidget(self.city_pages_list[-1])
        page.slider_btn.clicked.connect(self.sliderAnimation)
        if not is_added:
            page.add_btn.clicked.connect(lambda: self.addCity(page))
        else:
            if not page.getIsLocalCity():
                page.delete_btn.clicked.connect(lambda: self.deleteCity(page))

    def createWeatherFrame(self, page: WeatherPage):
        frame = WeatherFrame(self.scroll_area_widget, *page.getDataToWeatherFrame(), self.local_timezone_offset)
        self.city_frames_list.append(frame)
        frame.city_btn.clicked.connect(lambda: self.changePage(page))
        frame.temp_btn.clicked.connect(lambda: self.changePage(page))
        frame.time_btn.clicked.connect(lambda: self.changePage(page))
        frame.weather_btn.clicked.connect(lambda: self.changePage(page))
        page.timer.timeout.connect(lambda: frame.refreshData(*page.getDataToWeatherFrame()[1:5]))
        self.scroll_area_vlayout.addWidget(frame)

    def createPageFromSearch(self, city_country: str):
        """Create page from completer search"""
        city_name, country_name = city_country.split(", ")
        current_page = self.city_pages_list[self.stacked_widget.currentIndex()]
        current_page.weather_line_edit.setText("")
        if city_name == current_page.getCity() and country_name == current_page.getCountry():
            return

        for page in self.city_pages_list:
            if city_name == page.getCity() and country_name == page.getCountry():
                self.changePage(page)
                break
        else:
            index = bisect.bisect_left(self.cities_dict[country_name], city_name, key=lambda elem: elem.name)
            self.createPage(city_name, country_name,
                            self.cities_dict[country_name][index].lat, self.cities_dict[country_name][index].lon,
                            getWeatherData(self.cities_dict[country_name][index].lat,
                                           self.cities_dict[country_name][index].lon), False)

            self.changePage(self.city_pages_list[-1], True)

    def addCity(self, page: WeatherPage):
        """Overwrites user_data.json and create WeatherFrame object from page data"""
        page.setAdd(True)
        page.changeAddBtnToDeleteBtn()
        page.delete_btn.clicked.connect(lambda: self.deleteCity(page))

        city_dict = page.getCityDict()
        self.added_cities_list.append(city_dict)
        with open("data/user_data.json", "w", encoding="UTF-8") as fout:
            dump(self.added_cities_list, fout, ensure_ascii=False, indent="\t")

        self.scroll_area_vlayout.removeItem(self.spacerItem)
        self.createWeatherFrame(page)
        self.city_frames_list[-2].removeBorder()
        self.city_frames_list[-1].setFrameActive(True)
        self.scroll_area_vlayout.addItem(self.spacerItem)

    def deleteCity(self, page: WeatherPage):
        self.changePage(self.current_city_page)
        page_coord = page.getCityDict()["coord"]
        for i in range(len(self.added_cities_list)):
            if (self.added_cities_list[i]["coord"]["lat"] == page_coord["lat"] and
                    self.added_cities_list[i]["coord"]["lon"] == page_coord["lon"]):
                self.city_frames_list[i + 1].deleteLater()
                del self.city_frames_list[i + 1]

        self.stacked_widget.removeWidget(page)
        self.city_pages_list.remove(page)

        self.added_cities_list.remove(page.getCityDict())
        with open("data/user_data.json", "w", encoding="UTF-8") as fout:
            dump(self.added_cities_list, fout, ensure_ascii=False, indent="\t")

        page.deleteLater()

    def refreshFramesTime(self):
        current_time = QTime.currentTime()
        for frame in self.city_frames_list:
            frame.setTime(current_time)

    def createInternetWarningWindow(self):
        def btnsWork(btn):
            if btn.text() == "Retry":
                self.getCurrentLocation()
            else:
                exit(1)

        error = QtWidgets.QMessageBox()
        error.setWindowTitle("Нет подключения к интернету")
        error.setText("Проверьте подключение к интернету и нажмите Retry\nЕсли хотите закрыть приложение, нажмите Ok")
        error.setIcon(QtWidgets.QMessageBox.Warning)
        error.setStandardButtons(QtWidgets.QMessageBox.Retry | QtWidgets.QMessageBox.Ok)
        error.setDefaultButton(QtWidgets.QMessageBox.Retry)
        error.buttonClicked.connect(btnsWork)
        error.exec()


