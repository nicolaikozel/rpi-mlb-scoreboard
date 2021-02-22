from views.base_views import BaseView
from views.clock_view import ClockView


class MainView(BaseView):
    def render(self):
        ClockView(rgb_matrix=self._rgb_matrix).render()

