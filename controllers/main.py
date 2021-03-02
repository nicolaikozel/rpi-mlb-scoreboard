from rgbmatrix import RGBMatrix

from common.threading import RestartableThread
from controllers.base_controllers import BaseController
from controllers.looping_threads import LoopingThreadsController
from views.clock import ClockView
from views.weather import WeatherView


class MainController(BaseController):
    def __init__(self, rgb_matrix: RGBMatrix, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rgb_matrix = rgb_matrix
        self._clock_view_loop_controller = LoopingThreadsController(
            threads=[
                # RestartableThread(
                #    thread=ClockView,
                #    rgb_matrix=self._rgb_matrix,
                # ),
                RestartableThread(
                    thread=WeatherView,
                    rgb_matrix=self._rgb_matrix,
                ),
            ],
            thread_change_delay=1000,
        )
        self._set_current_thread(thread=self._clock_view_loop_controller)

    def _update_thread(self):
        pass
