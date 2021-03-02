from typing import Dict

from config import Config
from common.api_client import APIClient, RequestMethod


class OpenWeatherAPIClient(APIClient):
    api_key_param = "appid"

    @classmethod
    def _get_base_url(seclslf, *args, **kwargs) -> str:
        return "https://api.openweathermap.org/data/2.5/"

    @classmethod
    def _get_api_key(cls, *args, **kwargs) -> str:
        return Config.get()["weather"]["api_key"]

    @classmethod
    def get_current_weather(cls, location: str = None) -> Dict:
        config = Config.get()
        if not location:
            location = config["weather"]["location"]
        return cls._make_request(
            method=RequestMethod.GET,
            path="weather",
            params=dict(q=location, units=config["weather"]["units"]),
        )
