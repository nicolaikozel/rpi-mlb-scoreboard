from rgbmatrix import RGBMatrix

from common.threading import RestartableThread
from data import Data
from views.clock import ClockView
from views.controllers.base_controllers import BaseController
from views.controllers.looping_threads import LoopingThreadsController
from views.game_score import GameScoreView
from views.inning_score import InningScoreView
from views.upcoming_game import UpcomingGameView
from views.weather import WeatherView


class MainController(BaseController):
    def __init__(self, rgb_matrix: RGBMatrix, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rgb_matrix = rgb_matrix
        self._pre_game_loop_controller = RestartableThread(
            thread=LoopingThreadsController,
            threads=[
                {
                    "key": "clock",
                    "instance": RestartableThread(
                        thread=ClockView,
                        rgb_matrix=self._rgb_matrix,
                    ),
                },
                {
                    "key": "weather",
                    "instance": RestartableThread(
                        thread=WeatherView,
                        rgb_matrix=self._rgb_matrix,
                    ),
                },
            ],
            thread_change_delay=10,
        )
        self._game_in_progress_loop_controller = RestartableThread(
            thread=LoopingThreadsController,
            threads=[
                {
                    "key": "game_score",
                    "instance": RestartableThread(
                        thread=GameScoreView,
                        rgb_matrix=self._rgb_matrix,
                    ),
                },
                {
                    "key": "inning_score",
                    "instance": RestartableThread(
                        thread=InningScoreView,
                        rgb_matrix=self._rgb_matrix,
                    ),
                },
            ],
            thread_change_delay=5,
        )
        self._set_current_thread(thread=self._pre_game_loop_controller)

    def _update_thread(self):
        current_game = Data.get("current_game")
        games_today = Data.get("games_today")

        # GAME IN PROGRESS
        # ----------------
        if current_game:
            # Switch to the game in progress loop if we aren't showing it already
            if self._current_thread != self._game_in_progress_loop_controller:
                self._switch_thread(thread=self._game_in_progress_loop_controller)
        else:
            # UPCOMING GAME
            # -------------
            key = "upcoming_game"
            has_thread_for_upcoming_game = (
                self._pre_game_loop_controller.instance.has_thread_for_key(key=key)
            )
            if games_today and games_today.is_upcoming_game:
                # Add the upcoming game view to the pre-game loop
                # if it hasn't already been added
                if not has_thread_for_upcoming_game:
                    self._pre_game_loop_controller.instance.add_thread(
                        thread={
                            "key": key,
                            "instance": RestartableThread(
                                thread=UpcomingGameView,
                                rgb_matrix=self._rgb_matrix,
                            ),
                        },
                    )
            elif has_thread_for_upcoming_game:
                # Remove the upcoming game view from the pre-game loop
                self._pre_game_loop_controller.instance.remove_thread(key=key)

            # PRE GAME
            # --------
            # Switch to the pre-game loop if we were showing the game in progress loop
            if self._current_thread == self._game_in_progress_loop_controller:
                self._switch_thread(thread=self._pre_game_loop_controller)
