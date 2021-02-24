import time

from views.base_views import BaseView
from views.clock import ClockView


class MainView(BaseView):
    def render(self):
        clock_view = ClockView(rgb_matrix=self._rgb_matrix)
        while True:
            clock_view.render()
            time.sleep(0.05)

