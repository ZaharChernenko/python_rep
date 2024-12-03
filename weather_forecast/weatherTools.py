import gettext
import geocoder
import requests
from WeatherStructs import HourlyWeatherDataElem, DailyWeatherDataElem, FullWeatherData
from exceptions import IpReceivingError


def parseHourlyWeatherData(hourly_data):
    for i, hour in enumerate(hourly_data):
        hourly_data[i] = HourlyWeatherDataElem(dt=hour["dt"],
                                               temp=int(hour["temp"]),
                                               icon=hour["weather"][0]["icon"])


def parseDailyWeatherData(daily_data):
    for i, day in enumerate(daily_data):
        daily_data[i] = DailyWeatherDataElem(dt=day["dt"],
                                             average_temp=int(day["temp"]["day"]),
                                             max_temp=int(day["temp"]["max"]),
                                             min_temp=int(day["temp"]["min"]),
                                             icon=day["weather"][0]["icon"])


def getWeatherData(lat: float, lon: float) -> FullWeatherData:
    weather_translator = gettext.translation('weather', './locale', languages=['ru'])
    weather_translator.install()
    try:
        full_data = requests.get(f"https://openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&appid"
                                 f"=439d4b804bc8187953eb36d2a8c26a02").json()
        parseHourlyWeatherData(full_data["hourly"])
        parseDailyWeatherData(full_data["daily"])
        weather_data = FullWeatherData(cur_temp=int(full_data["current"]["temp"]),
                                       max_temp=int(full_data["daily"][0].max_temp),
                                       min_temp=int(full_data["daily"][0].min_temp),
                                       cur_weather=_(full_data["current"]["weather"][0]["description"]),
                                       hourly=full_data["hourly"], daily=full_data["daily"],
                                       icon=full_data["current"]["weather"][0]["icon"],
                                       timezone_offset=full_data["timezone_offset"])

        return weather_data

    except requests.ConnectionError:
        #createInternetWarningWindow()
        return getWeatherData(lat, lon)


def _getCurrentLocation():
    location = geocoder.ip('me')

    if location.city is None:
        raise IpReceivingError

    return location
