from enum import Enum


class WeatherCondition(Enum):
    CLEAR = "Clear"
    CLOUDS = "Clouds"
    RAIN = "Rainy"
    DRIZZLE = "Drizzle"
    THUNDERSTORM = "Thunderstorm"
    SNOW = "Snow"


class Weather:
    def __init__(self, temperature: int, condition: str):
        self.temperature = temperature
        try:
            self.condition = WeatherCondition(condition)
        except ValueError:
            self.condition = WeatherCondition.CLOUDS


class WeatherData:
    def __init__(self, current: Weather):
        self.current = current
