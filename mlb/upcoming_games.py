from datetime import datetime
from typing import List

import mlbgame

from config import Config
from common.threading import DataThread
from weather.data_classes import Weather, WeatherData


class UpcomingGamesDataThread(DataThread):
    def _fetch_data(self) -> List[mlbgame.game.GameScoreboard]:
        now = datetime.now()
        team = Config.get()["team"]
        games = mlbgame.day(
            year=now.year, month=now.month, day=now.day, home=team, away=team
        )
        return games
