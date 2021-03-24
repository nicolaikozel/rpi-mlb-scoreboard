from datetime import datetime
from typing import Optional

import mlbgame

from common.threading import DataThread
from mlb.data_classes import CurrentGameData


class CurrentGameDataThread(DataThread):
    def _fetch_data(self) -> Optional[CurrentGameData]:
        from data import Data

        games_today = Data.get("games_today")
        if games_today:
            active_game = games_today.active_game
            if active_game:
                overview = mlbgame.overview(active_game.game_id)
                return CurrentGameData(overview=overview)
        return None
