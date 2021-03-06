import time
from typing import Dict

from config import Config
from common.api_client import APIClient, RequestMethod
from common.threading import DataThread
from weather.data_classes import Weather, WeatherData


class OpenWeatherAPIClient(APIClient):
    api_key_param = "appid"

    @classmethod
    def _get_base_url(seclslf, *args, **kwargs) -> str:
        return "https://api.openweathermap.org/data/2.5/"

    @classmethod
    def _get_api_key(cls, *args, **kwargs) -> str:
        return Config.get()["weather"]["api_key"]

    @classmethod
    def get_current_weather(cls, location: str = None) -> Weather:
        config = Config.get()
        if not location:
            location = config["weather"]["location"]
        response = cls._make_request(
            method=RequestMethod.GET,
            path="weather",
            params=dict(q=location, units=config["weather"]["units"]),
        )
        return Weather(
            temperature=int(response["main"]["temp"]),
            condition=response["weather"][0]["main"],
        )


class OpenWeatherDataThread(DataThread):
    def _fetch_data(self) -> WeatherData:
        current_weather = OpenWeatherAPIClient.get_current_weather()
        return WeatherData(current=current_weather)
