from rgbmatrix import RGBMatrix

from common.threading import RestartableThread
from controllers.base_controllers import BaseController
from controllers.looping_threads import LoopingThreadsController
from data import Data
from views.clock import ClockView
from views.upcoming_game import UpcomingGameView
from views.weather import WeatherView


class MainController(BaseController):
    def __init__(self, rgb_matrix: RGBMatrix, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rgb_matrix = rgb_matrix
        self._main_loop_controller = LoopingThreadsController(
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
        self._set_current_thread(thread=self._main_loop_controller)

    def _update_thread(self):
        upcoming_games = Data.get("upcoming_games")
        key = "upcoming-games"
        has_thread_for_key = self._main_loop_controller.has_thread_for_key(key=key)
        if upcoming_games and not has_thread_for_key:
            self._main_loop_controller.add_thread(
                thread={
                    "key": key,
                    "instance": RestartableThread(
                        thread=UpcomingGameView,
                        rgb_matrix=self._rgb_matrix,
                        game=upcoming_games[0],
                    ),
                },
            )
            self._main_loop_controller.remove_thread(key="clock")
        elif not upcoming_games and has_thread_for_key:
            self._main_loop_controller.remove_thread(key=key)
