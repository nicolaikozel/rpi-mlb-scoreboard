from rgbmatrix import RGBMatrix

from common.threading import RestartableThread
from controllers.base_controllers import BaseController
from controllers.looping_views import LoopingViewsController
from views.clock import ClockView


class MainController(BaseController):
    def __init__(self, rgb_matrix: RGBMatrix, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rgb_matrix = rgb_matrix
        self._clock_loop_controller = LoopingViewsController(
            views=[
                RestartableThread(thread=ClockView, rgb_matrix=self._rgb_matrix, loc="Tor"),
                RestartableThread(thread=ClockView, rgb_matrix=self._rgb_matrix, loc="Ist"),
            ],
            view_change_delay=3,
        )
        self._active_thread = self._clock_loop_controller
    
    def _cleanup(self):
        self._active_thread.stop()
        self._active_thread.join()

    def _update_view(self):
        if not self._active_thread.is_alive():
            self._active_thread.start()