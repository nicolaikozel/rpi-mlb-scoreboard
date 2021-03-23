from datetime import datetime
from typing import Optional

import mlbgame

from common.threading import DataThread
from mlb.data_classes import CurrentGameData


class CurrentGameDataThread(DataThread):
    def _fetch_data(self) -> Optional[CurrentGameData]:
        upcoming_games = Data.get("upcoming_games")
        active_game = upcoming_games.active_game
        if active_game:
            innings = mlbgame.game_events(active_game.game_id)
            return CurrentGameData(innings=innings)
        return None
