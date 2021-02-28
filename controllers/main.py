from rgbmatrix import RGBMatrix

from common.threading import RestartableThread
from controllers.base_controllers import BaseController
from controllers.looping_threads import LoopingThreadsController
from views.clock import ClockView


class MainController(BaseController):
    def __init__(self, rgb_matrix: RGBMatrix, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rgb_matrix = rgb_matrix
        self._clock_view_loop_controller = LoopingThreadsController(
            threads=[
                RestartableThread(
                    thread=ClockView, rgb_matrix=self._rgb_matrix, loc="Tor"
                ),
                RestartableThread(
                    thread=ClockView, rgb_matrix=self._rgb_matrix, loc="Ist"
                ),
            ],
            thread_change_delay=3,
        )
        self._current_thread = self._clock_view_loop_controller

    @property
    def current_thread(self) -> BaseController:
        return self._current_thread

    def _update_thread(self):
        pass
