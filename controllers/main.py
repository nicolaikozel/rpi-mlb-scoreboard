from rgbmatrix import RGBMatrix

from common.threading import RestartableThread
from controllers.base_controllers import BaseController
from controllers.looping_threads import LoopingThreadsController
from data import Data
from views.clock import ClockView
from views.inning_score import InningScoreView
from views.upcoming_game import UpcomingGameView
from views.weather import WeatherView


class MainController(BaseController):
    def __init__(self, rgb_matrix: RGBMatrix, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rgb_matrix = rgb_matrix
        self._pre_game_loop_controller = LoopingThreadsController(
            threads=[
                {
                    "key": "clock",
                    "instance": RestartableThread(
                        thread=ClockView, rgb_matrix=self._rgb_matrix,
                    ),
                },
                {
                    "key": "weather",
                    "instance": RestartableThread(
                        thread=WeatherView, rgb_matrix=self._rgb_matrix,
                    ),
                },
            ],
            thread_change_delay=10,
        )
        self._game_in_progress_loop_controller = LoopingThreadsController(
            threads=[
                {
                    "key": "inning_score",
                    "instance": RestartableThread(
                        thread=InningScoreView, rgb_matrix=self._rgb_matrix,
                    ),
                },
            ],
            thread_change_delay=10,
        )
        self._set_current_thread(thread=self._pre_game_loop_controller)

    def _update_thread(self):
        games_today = Data.get("games_today")
        active_game = games_today.active_game

        # Render game in progress loop
        if (
            active_game
            and self._current_thread != self._game_in_progress_loop_controller
        ):
            self._switch_thread(thread=self._game_in_progress_loop_controller)

        # Render game schedule
        key = "upcoming-game"
        has_thread_for_key = self._pre_game_loop_controller.has_thread_for_key(key=key)
        if games_today and not active_game and not has_thread_for_key:
            self._pre_game_loop_controller.add_thread(
                thread={
                    "key": key,
                    "instance": RestartableThread(
                        thread=UpcomingGameView,
                        rgb_matrix=self._rgb_matrix,
                        game=games_today.next_game,
                    ),
                },
            )
        elif has_thread_for_key:
            self._pre_game_loop_controller.remove_thread(key=key)
