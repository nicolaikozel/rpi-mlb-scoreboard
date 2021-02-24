from views.base_views import BaseView
from views.clock import ClockView


class MainView(BaseView):
    def render(self):
        ClockView(rgb_matrix=self._rgb_matrix).render()

