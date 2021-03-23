from datetime import datetime
from typing import List

import mlbgame

from config import Config
from common.threading import DataThread
from mlb.data_classes import UpcomingGamesData


class UpcomingGamesDataThread(DataThread):
    def _fetch_data(self) -> UpcomingGamesData:
        now = datetime.now()
        team = Config.get()["team"]
        games = mlbgame.day(
            year=now.year, month=now.month, day=now.day, home=team, away=team
        )
        return UpcomingGamesData(games=games)
