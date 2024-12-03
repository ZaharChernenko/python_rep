from typing import NamedTuple


Celsius = int
WeatherType = str


class HourlyWeatherDataElem(NamedTuple):
    dt: int
    temp: Celsius
    icon: str


class DailyWeatherDataElem(NamedTuple):
    dt: int
    average_temp: Celsius
    max_temp: Celsius
    min_temp: Celsius
    icon: str


class FullWeatherData(NamedTuple):
    cur_temp: Celsius
    max_temp: Celsius
    min_temp: Celsius
    cur_weather: WeatherType
    hourly: list[HourlyWeatherDataElem]
    daily: list[DailyWeatherDataElem]
    icon: str
    timezone_offset: int
