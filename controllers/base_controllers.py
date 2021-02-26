import time
from abc import ABC, abstractmethod

from common.threading import StoppableThread


class BaseController(StoppableThread, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._loop_count = 0

    @abstractmethod
    def _update_view(self):
        pass

    def run(self):
        while True:
            self._update_view()
            time.sleep(1)
            self._loop_count += 1
            if self.stopped:
                break