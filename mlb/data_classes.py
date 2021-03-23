from datetime import datetime
from typing import List, Optional

import mlbgame


class UpcomingGamesData:
    def __init__(self, games: List[mlbgame.game.GameScoreboard]):
        self.games = games

    @property
    def next_game(self) -> Optional[mlbgame.game.GameScoreboard]:
        for game in self.games:
            if game.game_start_time > datetime.now():
                return game
        return None

    @property
    def active_game(self) -> Optional[mlbgame.game.GameScoreboard]:
        for game in self.games:
            if game.game_status == "IN_PROGRESS":
                return game
        return None


class CurrentGameData:
    def __init__(self, innings: List[mlbgame.events.Inning]):
        self.innings = innings

    @property
    def current_inning(self) -> mlbgame.events.Inning:
        return self.innings[-1]

    @property
    def is_top_of_inning(self):
        return not self.current_inning.bottom

    @property
    def current_at_bat(self) -> Optional[mlbgame.events.AtBat]:
        current_inning = self.current_inning
        half = current_inning.top if self.is_top_of_inning else current_inning.bottom
        for item in reversed(half):
            if isinstance(item, mlbgame.events.AtBat):
                return item
        return None
