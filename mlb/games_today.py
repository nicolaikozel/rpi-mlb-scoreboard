from datetime import datetime
from typing import List

import mlbgame

from config import Config
from common.threading import DataThread
from mlb.data_classes import GamesTodayData


class GamesTodayDataThread(DataThread):
    def _fetch_data(self) -> GamesTodayData:
        now = datetime.now()
        team = Config.get()["team"]
        games = mlbgame.day(
            year=now.year, month=now.month, day=now.day, home=team, away=team
        )
        return GamesTodayData(games=games)
