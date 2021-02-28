import time

from controllers.base_controllers import BaseController


class LoopingViewsController(BaseController):
    def __init__(self, views, view_change_delay, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._views = views
        self._view_index = 0
        self._view_change_delay = view_change_delay
    
    @property
    def current_view(self):
        return self._views[self._view_index]

    def _cleanup(self):
        self.current_view.stop()
        self.current_view.join()

    def _switch_view(self, view):
        if self.current_view:
            self.current_view.stop()
            self.current_view.join()
        view.reset()
        view.start()

    def _switch_to_next_view(self):
        next_view_index = self._view_index + 1
        if next_view_index == len(self._views):
            next_view_index = 0
        self._switch_view(view=self._views[next_view_index])
        self._view_index = next_view_index

    def _update_view(self):
        if not self.current_view.is_alive():
            self.current_view.start()
        elif self._loop_count % self._view_change_delay == 0:
            self._switch_to_next_view()