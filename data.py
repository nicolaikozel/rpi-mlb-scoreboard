from mlb.current_game import CurrentGameDataThread
from mlb.games_today import GamesTodayDataThread
from weather.open_weather import OpenWeatherDataThread


class Data:
    _data = {
        "current_game": CurrentGameDataThread(refresh_rate=5, daemon=True),
        "games_today": GamesTodayDataThread(refresh_rate=300, daemon=True),
        "weather": OpenWeatherDataThread(refresh_rate=30, daemon=True),
    }

    @classmethod
    def get(cls, key: str) -> object:
        return cls._data[key].data

    @classmethod
    def start_all_data_threads(cls):
        for thread in cls._data.values():
            thread.start()
