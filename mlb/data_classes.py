from datetime import datetime
from typing import List, Optional, Tuple

import mlbgame

from mlb.constants import Base, InningState


class GamesTodayData:
    def __init__(self, games: List[mlbgame.game.GameScoreboard]):
        self.games = games

    @property
    def upcoming_game(self) -> Optional[mlbgame.game.GameScoreboard]:
        for game in self.games:
            if game.date > datetime.now():
                return game
        return None

    @property
    def is_upcoming_game(self) -> bool:
        return bool(self.upcoming_game)

    @property
    def active_game(self) -> Optional[mlbgame.game.GameScoreboard]:
        for game in self.games:
            if game.game_status == "IN_PROGRESS":
                return game
        return None


class CurrentGameData:
    def __init__(self, overview: mlbgame.game.Overview):
        self.overview = overview

    def is_runner_on_base(self, base: Base) -> bool:
        return bool(getattr(self.overview, f"runner_on_{base.value}", None))

    @property
    def inning_and_state(self) -> Tuple[int, InningState]:
        return self.overview.inning, InningState(self.overview.inning_state)

    @property
    def pitch_count(self) -> str:
        return f"{self.overview.balls}-{self.overview.strikes}"
